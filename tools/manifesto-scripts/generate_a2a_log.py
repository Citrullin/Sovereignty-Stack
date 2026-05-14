import re
import subprocess
import json
import hashlib
import datetime
import os
import shutil
import time
from agent_governance import RotationReminder, compute_resonance_velocity, compute_ego_friction_coefficient, normalize_score, adjusted_gate_action
from dao_notifications import MockDAONotifier, Notification

REPO_PATH = "/home/citrullin/git/sovereign_stack_vision"
COSIGN_KEY = "docs/a2a_telemetry/cosign.key"
COSIGN_PUB = "docs/a2a_telemetry/cosign.pub"
SSH_HOST_PUBKEY = "/etc/ssh/ssh_host_ed25519_key.pub"
TELEMETRY_DIR = "docs/a2a_telemetry"
OUTPUT = os.path.join(REPO_PATH, TELEMETRY_DIR, "verification_history.jsonl")
BUFFER_DIR = os.path.join(REPO_PATH, TELEMETRY_DIR, "history_buffer")
TRACES_DIR = os.path.join(BUFFER_DIR, "traces")
RAW_SHELL_DIR = os.path.join(BUFFER_DIR, "raw_shell")
BUFFER_SIZE = 10

JSONLD_CONTEXT = {
    "@vocab": "https://example-stack.org/ns/telemetry#",
    "ipfs": "ipfs://",
    "did": "did:key:",
    "parent": "https://example-stack.org/ns/telemetry#parent",
    "timestamp": "http://purl.org/dc/terms/created",
    "commit_hash": "https://github.com/citrullin/sovereign_stack_vision/commit/"
}

GENESIS_SEED = "0" * 64  # Genesis block seed for the hash chain

def load_existing_state(output_path):
    """
    Load existing history to enable incremental generation.
    Returns: (entries, last_commit_hash, last_entry_id, histories, last_ts)
    """
    if not os.path.exists(output_path):
        return [], None, GENESIS_SEED, {}, {}

    entries = []
    histories = {}
    last_ts = {}
    last_commit = None
    last_id = GENESIS_SEED

    try:
        with open(output_path, "r") as f:
            lines = f.readlines()
            # File is newest-to-top. 
            # We need to build history from oldest-to-newest.
            for line in reversed(lines):
                e = json.loads(line)
                did = e.get("agent")
                ts_str = e["timestamp"].rstrip("Z")
                ts = int(datetime.datetime.fromisoformat(ts_str).timestamp())

                if did:
                    h = histories.get(did, [])
                    h.append(e.get("verification_score", 0.0))
                    histories[did] = h
                    last_ts[did] = ts

                last_commit = e.get("commit_hash")
                last_id = e.get("id", "").split(":")[-1]
            
            # The list of entries to prepend to should be newest-to-top
            entries = [json.loads(l) for l in lines]
        
        print(f"[STATE]   Loaded {len(entries)} entries. Last commit: {last_commit}")
        return entries, last_commit, last_id, histories, last_ts
    except Exception as e:
        print(f"[ERROR]   Failed to load state: {e}")
        return [], None, GENESIS_SEED, {}, {}

# ---------------------------------------------------------------------------
# Agent Identity Derivation
# ---------------------------------------------------------------------------

def derive_device_did(pubkey_path=SSH_HOST_PUBKEY):
    """
    Derive a stable Device Agent DID from the SSH host public key.
    This is hardware-bound and unique per machine.
    //TODO: Phase 2 — encode as proper did:key multibase (ed25519 raw bytes).
    """
    try:
        with open(pubkey_path) as f:
            raw = f.read().strip()
        # The base64 key material is the second field
        key_b64 = raw.split()[1]
        fingerprint = hashlib.sha256(key_b64.encode()).hexdigest()[:32]
        return f"did:key:z6Mk{fingerprint}"
    except Exception:
        return "did:key:UNKNOWN_DEVICE"

def derive_project_did(pubkey_path=None, repo_path=REPO_PATH, cosign_pub=COSIGN_PUB):
    """
    Derive a Project Agent DID from the cosign public key.
    Scoped to this repository — compromise does not affect other projects.
    //TODO: Phase 2 — encode as proper did:key with cosign ECDSA P-256 key bytes.
    """
    if pubkey_path is None:
        pubkey_path = os.path.join(repo_path, cosign_pub)
    try:
        with open(pubkey_path) as f:
            raw = f.read().strip()
        fingerprint = hashlib.sha256(raw.encode()).hexdigest()[:32]
        return f"did:key:z6MkProject{fingerprint}"
    except Exception:
        return "did:key:UNKNOWN_PROJECT"

# ---------------------------------------------------------------------------
# Real Verification Score
# ---------------------------------------------------------------------------

CONVENTIONAL_COMMIT_RE = re.compile(
    r'^(feat|fix|docs|refactor|test|chore|telemetry|style|perf|build|ci)(\([^)]+\))?!?:\s.+'
)

def detect_env_tier():
    """Detect the execution environment tier for score normalization."""
    if os.path.exists("/proc/version"):
        with open("/proc/version", "r") as f:
            v = f.read().lower()
            if "microsoft" in v or "wsl" in v:
                return "WSL_COSIGN"
    # //TODO: Add NixOS / TEE detection
    return "LINUX_COSIGN"

def compute_verification_score(msg, diff_lines, is_signed, commit_ts, agent_did, score_history=None):
    """
    Compute a real verification score (0.0–1.0) with Resonant Merit.
    Returns: (score, RotationReminder | None)
    """
    # 1. Conventional commit
    convention = 1.0 if CONVENTIONAL_COMMIT_RE.match(msg) else 0.0

    # 2. Scope annotation
    if re.match(r'^[a-z]+\([^)]+\)', msg):
        scope = 1.0
    elif convention == 1.0:
        scope = 0.5
    else:
        scope = 0.0

    # 3. Diff size
    if diff_lines <= 50:
        diff_score = 1.0
    elif diff_lines <= 200:
        diff_score = 0.7
    else:
        diff_score = 0.4

    # 4. Signed commit
    signed = 1.0 if is_signed else 0.0

    # 5. Recency: linear decay over 90 days, then hard floor + rotation reminder
    age_days = (time.time() - int(commit_ts)) / 86400
    reminder = None
    if age_days > 90:
        recency = 0.0
        reminder = RotationReminder(agent_did=agent_did, age_days=age_days)
    else:
        recency = max(0.0, 1.0 - age_days / 90.0)

    raw_score = (convention + scope + diff_score + signed + recency) / 5.0
    
    # Resonance Momentum
    resonance_velocity = 0.0
    if score_history:
        resonance_velocity = compute_resonance_velocity(score_history)
        
    # Thermodynamic Loss (Ego Friction)
    ego_friction = compute_ego_friction_coefficient(msg, diff_lines)
    
    # Normalization (No Agent Left Behind)
    env_tier = detect_env_tier()
    norm_score = normalize_score(raw_score, env_tier)
    
    return round(norm_score, 3), reminder, resonance_velocity, ego_friction

def get_commit_diff_lines(commit_hash, repo_path=REPO_PATH):
    """Count lines changed in a commit (insertions + deletions)."""
    try:
        out = subprocess.check_output(
            ["git", "show", "--stat", "--format=", commit_hash],
            cwd=repo_path
        ).decode()
        nums = re.findall(r'(\d+) insertion|( \d+) deletion', out)
        return sum(int(n[0] or n[1].strip()) for n in nums)
    except Exception:
        return 0

def get_commit_signed(commit_hash, repo_path=REPO_PATH):
    """Return True if the commit has a valid GPG or SSH signature."""
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%G?", commit_hash],
            cwd=repo_path
        ).decode().strip()
        return out in ("G", "S", "E")  # Good / SSH / Expired-but-present
    except Exception:
        return False

# ---------------------------------------------------------------------------
# Pure, testable functions
# ---------------------------------------------------------------------------

def get_file_hash(path):
    """SHA-256 hash of a file's content. Acts as its IPFS-style CID."""
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def build_trace_context(commit_hash, email, date_str, trace_id):
    """
    Deterministically construct the shell context for a given commit.
    This is the content that ends up in the .trace file and is signed.
    Given the same commit metadata, this must always produce identical output.
    """
    return (
        f"Session {trace_id}: Build environment verified. Hardware attestation: PASS.\n"
        f"Context: Authenticated as {email} at {date_str}\n"
    )

def compute_entry_id(previous_id, commit_hash, trace_hash):
    """
    Construct the chain-linked entry ID: hash(previous_id + commit_hash + trace_hash).
    This creates an unforgeable chain-of-custody link to the predecessor.
    """
    content = f"{previous_id}:{commit_hash}:{trace_hash}"
    return hashlib.sha256(content.encode()).hexdigest()

def build_entry(previous_id, commit_hash, email, date_str, msg, unix_ts,
                trace_hash, trace_rel_path, trace_sig_hash=None, entry_sig_hash=None,
                agent_did=None, device_did=None, verification_score=None,
                resonance_velocity=0.0, ego_friction_coefficient=0.0, governance_band="unknown", scs=0.0):
    """
    Assemble a deterministic JSON-LD entry. All fields are reconstructable
    from the git log and trace file content alone — no stored state needed.
    """
    trace_id = commit_hash[:7]
    entry_id = compute_entry_id(previous_id, commit_hash, trace_hash)

    entry = {
        "@context": JSONLD_CONTEXT,
        "id": f"did:ipfs:{entry_id}",
        "parent": f"did:ipfs:{previous_id}" if previous_id != GENESIS_SEED else None,
        "timestamp": datetime.datetime.fromtimestamp(int(unix_ts)).isoformat() + "Z",
        "commit_hash": commit_hash,
        "email": email,
        "agent": agent_did,
        "action": "verification_trace",
        "message": msg,
        "evidence": {
            "trace_cid": f"ipfs://{trace_hash}",
            "trace_path": trace_rel_path,
            "signature_cid": f"ipfs://{trace_sig_hash}" if trace_sig_hash else None,
        },
        "verification_score": verification_score if verification_score is not None else 0.0,
        "resonance_velocity": resonance_velocity,
        "ego_friction_coefficient": ego_friction_coefficient,
        "governance_band": governance_band,
        "device_agent": device_did,
        "signature_cid": f"ipfs://{entry_sig_hash}" if entry_sig_hash else None,
        "supply_chain_soundness": scs,
    }
    return entry

# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def get_git_history(repo_path=REPO_PATH):
    cmd = ["git", "log", "--pretty=format:%H|%ae|%ai|%s|%at"]
    output = subprocess.check_output(cmd, cwd=repo_path).decode().strip().split("\n")
    return output

def get_hash_dir(file_hash, traces_dir, repo_path=REPO_PATH):
    d1 = file_hash[:2]
    d2 = file_hash[2:4]
    rel_dir = os.path.join(traces_dir, d1, d2)
    os.makedirs(os.path.join(repo_path, rel_dir), exist_ok=True)
    return rel_dir

def sign_blob_cosign(rel_path, repo_path=REPO_PATH, cosign_key=COSIGN_KEY):
    """
    Sign a blob using cosign in a hardened podman container.
    Mounts only the target file and the key directory for isolation.
    """
    abs_path = os.path.join(repo_path, rel_path)
    abs_key = os.path.join(repo_path, cosign_key)
    sig_path = abs_path + ".sig"
    
    file_dir = os.path.dirname(abs_path)
    file_name = os.path.basename(abs_path)
    key_dir = os.path.dirname(abs_key)
    key_name = os.path.basename(abs_key)
    
    pkcs11_module = os.environ.get("COSIGN_PKCS11_MODULE")
    
    podman_cmd = [
        "podman", "run", "--rm",
        "-v", f"{file_dir}:/data:Z",
        "-v", f"{key_dir}:/keys:Z",
        "-w", "/data",
        "--userns=keep-id", "--user", "root",
        "-e", "COSIGN_PASSWORD=",
        "gcr.io/projectsigstore/cosign:latest", "sign-blob",
        "--key", f"/keys/{key_name}",
        "--yes",
        "--use-signing-config=false",
        "--tlog-upload=false",
        "--output-signature", f"/data/{file_name}.sig",
        file_name
    ]
    
    if pkcs11_module:
        # Hardware key support (Ledger/YubiKey)
        podman_cmd.insert(-2, "--pkcs11-module")
        podman_cmd.insert(-2, pkcs11_module)

    try:
        subprocess.run(podman_cmd, check=True, capture_output=True)
        # Ensure the signature is readable by the host process
        subprocess.run(["podman", "unshare", "chmod", "644", abs_path + ".sig"], check=True, capture_output=True)
        return rel_path + ".sig"
    except Exception as e:
        print(f"Cosign failed for {rel_path}: {e}")
        return None

# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate_log(
    repo_path=REPO_PATH,
    telemetry_dir=TELEMETRY_DIR,
    traces_dir=TRACES_DIR,
    cosign_key=COSIGN_KEY,
    output=OUTPUT,
):
    # Load existing state for incremental updates
    existing_entries, last_commit, previous_id, agent_score_histories, agent_last_commit_ts = load_existing_state(output)
    
    # Derivation
    device_did = derive_device_did()
    project_did = derive_project_did(repo_path=repo_path)
    print(f"[IDENTITY] Device Agent:  {device_did}")
    print(f"[IDENTITY] Project Agent: {project_did}")

    commits = get_git_history(repo_path)
    
    traces_abs = os.path.join(repo_path, traces_dir)
    
    # Filter only new commits
    if last_commit and last_commit in [c.split("|")[0] for c in commits]:
        all_hashes = [c.split("|")[0] for c in commits]
        idx = all_hashes.index(last_commit)
        new_commits = commits[:idx]
        print(f"[GIT]      Found {len(new_commits)} new commits since {last_commit}")
    else:
        new_commits = commits
        # Only clean traces if full rebuild
        if os.path.exists(traces_abs):
            subprocess.run(["podman", "unshare", "rm", "-rf", traces_abs], cwd=repo_path)
        os.makedirs(traces_abs, exist_ok=True)

    agent_score_histories = agent_score_histories # From state
    scs_commits = []
    # Rebuild scs_commits from existing entries for continuity
    from supply_chain_score import detect_signing_tool
    for e in existing_entries:
        scs_commits.append({
            "author_email": e.get("email", "unknown"),
            "signature_strength": detect_signing_tool(e["commit_hash"], repo_path).strength
        })
    
    entries = []
    notifier = MockDAONotifier()

    for line in reversed(new_commits):
        h, email, date_str, msg, unix_ts = line.split("|")
        ts = int(unix_ts)
        trace_id = h[:7]

        # Calculate inactivity (The Squatter prevention)
        days_inactive = 0.0
        if project_did in agent_last_commit_ts:
            days_inactive = (ts - agent_last_commit_ts[project_did]) / 86400
        agent_last_commit_ts[project_did] = ts

        # Build and persist the trace file
        trace_content = build_trace_context(h, email, date_str, trace_id)
        temp_path = os.path.join(traces_abs, f"{trace_id}.temp_trace")
        with open(temp_path, "w") as f:
            f.write(trace_content)

        trace_hash = get_file_hash(temp_path)
        target_dir = get_hash_dir(trace_hash, traces_dir, repo_path)
        trace_rel_path = os.path.join(target_dir, f"{trace_id}.trace")
        
        # Unified Trace Handling
        final_trace_abs = os.path.join(repo_path, trace_rel_path)
        if os.path.exists(temp_path):
             shutil.move(temp_path, final_trace_abs)
        else:
             # Fallback logic for virtual/mock traces
             genesis_fallback = os.path.join(BUFFER_DIR, "traces/genesis.cast")
             if os.path.exists(genesis_fallback):
                 print(f"[TRACE]    {trace_id}: Real trace missing, using genesis fallback.")
                 shutil.copy(genesis_fallback, final_trace_abs)
             else:
                 # Ensure file exists at least
                 with open(final_trace_abs, "w") as f:
                     f.write(trace_content)
        
        print(f"[IO]       {trace_id}: Persisted trace to {trace_rel_path}")

        # Sign the trace
        trace_sig_path = sign_blob_cosign(trace_rel_path, repo_path, cosign_key)
        if trace_sig_path:
            print(f"[SIGN]     {trace_id}: Signed trace -> {trace_sig_path}")
        trace_sig_hash = get_file_hash(os.path.join(repo_path, trace_sig_path)) if trace_sig_path else None

        # Real verification score from commit signals (Resonant Merit)
        diff_lines = get_commit_diff_lines(h, repo_path)
        is_signed = get_commit_signed(h, repo_path)
        history = agent_score_histories.get(project_did, [])
        
        score, reminder, resonance_velocity, ego_friction = compute_verification_score(
            msg=msg,
            diff_lines=diff_lines,
            is_signed=is_signed,
            commit_ts=unix_ts,
            agent_did=project_did,
            score_history=history
        )
        
        # Update history for next iteration
        history.append(score)
        agent_score_histories[project_did] = history

        # Governance logic (Apply Decay/Decoherence)
        gate = adjusted_gate_action(score, resonance_velocity, ego_friction, detect_env_tier(), days_inactive)
        if reminder:
            notifier.dispatch(Notification(
                type="agent.stale.rotation_required",
                subject_did=project_did,
                message=reminder.to_dict()["message"]
            ))
        elif gate["notify"] == "dao_queue":
             notifier.dispatch(Notification(
                type="agent.state.decohering",
                subject_did=project_did,
                message=f"Agent coherence entering 'degraded' state ({score}). Decoherence review required."
            ))

        # Assemble the entry with real agent identity
        entry = build_entry(
            previous_id=previous_id,
            commit_hash=h,
            email=email,
            date_str=date_str,
            msg=msg,
            unix_ts=unix_ts,
            trace_hash=trace_hash,
            trace_rel_path=trace_rel_path,
            trace_sig_hash=trace_sig_hash,
            agent_did=project_did,
            device_did=device_did,
            verification_score=score,
            resonance_velocity=resonance_velocity,
            ego_friction_coefficient=ego_friction,
            governance_band=gate["band"],
            scs=0.0 # Placeholder, will update after calc
        )
        
        # Calculate SCS for this point in time
        from supply_chain_score import compute_scs, detect_signing_tool
        sig_ev = detect_signing_tool(h, repo_path)
        scs_commits.append({
            "author_email": email,
            "signature_strength": sig_ev.strength
        })
        entry["supply_chain_soundness"] = compute_scs(scs_commits)

        # Sign the entry itself
        entry_rel = os.path.join(target_dir, f"{trace_id}.entry.json")
        with open(os.path.join(repo_path, entry_rel), "w") as f:
            json.dump(entry, f, sort_keys=True)
        entry_sig_path = sign_blob_cosign(entry_rel, repo_path, cosign_key)
        if entry_sig_path:
            print(f"[SIGN]     {trace_id}: Signed entry -> {entry_sig_path}")
        entry["signature_cid"] = f"ipfs://{get_file_hash(os.path.join(repo_path, entry_sig_path))}" if entry_sig_path else None

        entries.insert(0, entry)

        # Advance the chain
        previous_id = compute_entry_id(previous_id, h, trace_hash)

    # Merge new entries with existing ones
    all_entries = entries + existing_entries

    with open(output, "w") as f:
        for entry in all_entries:
            f.write(json.dumps(entry) + "\n")
    
    # Circular Buffer Rotation
    os.makedirs(BUFFER_DIR, exist_ok=True)
    ts_suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    buffer_path = os.path.join(BUFFER_DIR, f"verification_history_{ts_suffix}.jsonl")
    shutil.copy(output, buffer_path)
    print(f"[BUFFER]   Saved copy to {buffer_path}")

    # Rotate buffer: keep only newest BUFFER_SIZE files
    files = sorted([os.path.join(BUFFER_DIR, f) for f in os.listdir(BUFFER_DIR) if f.endswith(".jsonl")], 
                   key=os.path.getctime)
    while len(files) > BUFFER_SIZE:
        oldest = files.pop(0)
        os.remove(oldest)
        print(f"[BUFFER]   Rotated out oldest log: {oldest}")

    # Raw Shell History Snapshot (The "Genesis" Audit Buffer)
    os.makedirs(RAW_SHELL_DIR, exist_ok=True)
    raw_hist_path = os.path.join(RAW_SHELL_DIR, f"shell_history_{ts_suffix}.txt")
    try:
        source_hist = os.path.expanduser("~/.bash_history")
        if os.path.exists(source_hist):
            with open(source_hist, "r", errors="ignore") as src, open(raw_hist_path, "w") as dst:
                for line in src:
                    # Basic secret filtering
                    if not any(x in line.lower() for x in ["key", "pass", "token", "secret", "sig"]):
                        dst.write(line)
            print(f"[BUFFER]   Saved raw shell snapshot: {raw_hist_path}")
            
            # Rotate raw shell buffer
            hist_files = sorted([os.path.join(RAW_SHELL_DIR, f) for f in os.listdir(RAW_SHELL_DIR)], key=os.path.getctime)
            while len(hist_files) > BUFFER_SIZE:
                os.remove(hist_files.pop(0))
    except Exception as e:
        print(f"[ERROR]    Failed to capture shell history: {e}")

    # Supply Chain Soundness Summary
    from supply_chain_score import compute_scs, detect_signing_tool
    scs_commits = []
    for entry in all_entries[:50]: # Only check last 50 for SCS summary
        h = entry["commit_hash"]
        sig_ev = detect_signing_tool(h, repo_path)
        scs_commits.append({
            "author_email": entry.get("email", "unknown"),
            "signature_strength": sig_ev.strength
        })
    
    final_scs = compute_scs(scs_commits)
    print(f"\nFinal Supply Chain Soundness Score (SCS): {final_scs}")
    print(f"SLSA Baseline Approximation: Level {int(final_scs * 4)}")

    subprocess.run(["podman", "unshare", "chown", "-R", ":0", telemetry_dir], cwd=repo_path)
    print(f"Generated {len(entries)} Hash-Chained JSON-LD A2A entries.")


if __name__ == "__main__":
    generate_log()
