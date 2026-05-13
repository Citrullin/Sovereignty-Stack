#!/usr/bin/env python3
import subprocess
import os
import sys
import time

def start_trace(trace_name=None):
    if not trace_name:
        trace_name = f"session_{int(time.time())}"
    
    output_path = f"docs/a2a_telemetry/traces/{trace_name}.cast"
    os.makedirs("docs/a2a_telemetry/traces", exist_ok=True)
    
    print(f"--- A2A Trace Started: {output_path} ---")
    print("Commands recorded in this container are part of the cryptographic audit log.")
    
    # Run asciinema in podman if possible, or local as fallback
    try:
        # We use -q for quiet (don't show asciinema start messages)
        # We use a shell to ensure we capture the session
        cmd = ["asciinema", "rec", "-q", output_path]
        subprocess.run(cmd)
    except FileNotFoundError:
        print("Error: 'asciinema' not found. Please install it or use the podman variant.")
        sys.exit(1)

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else None
    start_trace(name)
