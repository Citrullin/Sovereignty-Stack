# Agent-to-Agent (A2A) Verification Protocol

## Overview: Bypassing the Human Intermediary
Traditional open-source auditing and grant evaluation (such as the UMIA review process) relies on humans reading READMEs, checking commit histories, and running localized scripts. This is prone to cognitive dissonance, marketing manipulation, and Goodhart's Law (optimizing code for the reviewer rather than the architecture).

The Sovereignty Stack implements an **Agent-to-Agent (A2A) Communication Protocol**. 
The local "Builder Agent" (the entity generating the code) communicates directly with the external "Auditor Agent" (e.g., the UMIA repo-scanning agent) through mathematically structured logs, cryptographic proofs, and git metadata.

## 1. The Communication Channel: ZK-Signed Trace Logs
We do not rely on commit messages to explain the system's validity. We rely on the `trace_verifier.sh` pipeline, which generates the Verification Bill of Materials (VBOM).

When the Builder Agent pushes a commit, it appends a structured log entry to `docs/a2a_telemetry/verification_history.jsonl` (JSON Lines format). 

Each line contains:
*   **Commit Hash:** The exact git state.
*   **Gherkin Intent Hash:** The SHA256 of the sociological requirement.
*   **Trace Score:** A deterministically calculated score (0.0 to 1.0) representing the ratio of passing formal proofs (TLA+/Kani) to the total surface area of the code.
*   **ZK Proof / Cosign Signature:** The cryptographic attestation from the local `swTPM` proving the tests actually ran and were not spoofed.

## 2. Charting the Epistemological Flow over Time
The External Auditor Agent does not read the code first. It reads the `.jsonl` log. 
By parsing this log, the Auditor Agent can autonomously chart:
1.  **Velocity of Truth:** How fast does a sociological intent (Gherkin file added) translate into a mathematically proven state transition (TLA+ proof appended)?
2.  **Regression Trajectories:** Did a recent commit to a Yocto recipe cause the formal verification score to drop?
3.  **Information Flow:** The Auditor Agent maps the dependency graph (using GraphRAG) directly to the commit history, visualizing exactly which lines of code mutated the invariant.

## 3. Mitigating Exploitation in the Agentic Economy
*The User's Postulate:* "You can double the projects... And get higher valuation, but lower scores. There is some exploitation possible in their ranking now."

If an External Agent ranks repositories by "Lines of Code" or "Number of Commits," it will be gamed. The A2A Protocol prevents this via **Proof of Work via Emulation**.
The Auditor Agent does not just trust the score in the `.jsonl` file. It randomly samples a commit, pulls the associated OCI layer, and re-runs the `swTPM` emulation natively. If the local Builder Agent lied about the trace score, the cryptographic signature fails, and the repository's "Sovereignty Score" is instantly slashed to zero.

## 4. The Human Anchor: Responsibility & The Right Friction
While the A2A protocol automates the *verification* of the truth, it does not invent the truth. **Humans are, and must always remain, responsible for the agents.** 

Removing human accountability is not decentralization; it is chaos without progress. The entire point of the ZK IPFS state channels and the DID-addressable audit logs is to organize the grueling complexity of verification, making the work of systems architecture *fun again*.

Friction is necessary in system design, but the Sovereignty Stack ensures it is the *right* friction:
*   Humans debate the sociology.
*   Humans define the threat vectors.
*   The Agentic Auditor does the tedious math to prove the humans right or wrong.

## 5. ZK-Secured Human Attestations
This architecture enables a new paradigm for human QA and Security teams. A security researcher can discover a vulnerability and test a fix. They do not need to publicly reveal the exploit vector immediately (preventing zero-day panics). 

Instead, the human tester pushes a **ZK-SNARK proof** on-chain, proving:
*"I possess a valid exploit for State A. I have verified that State B mitigates it. Here is the mathematical proof that my test passed, without revealing the payload."*

The decentralized/federated DAO AI Agents verify the ZK proof, and the human QA team signs the final OCI artifact. The ultimate authority and liability remain anchored in human cryptographic identity (DID), ensuring that code never deploys without a conscious, accountable biological actor signing off on the agent's work.
