#!/usr/bin/env python3
import json
import time
import os
import subprocess
import sys

def generate_mock_asciinema(commands, output_path):
    """Generates a simple v2 asciinema cast file."""
    header = {"version": 2, "width": 80, "height": 24, "timestamp": int(time.time()), "title": "A2A Verification Session"}
    with open(output_path, 'w') as f:
        f.write(json.dumps(header) + "\n")
        curr_time = 0.1
        for cmd in commands:
            # Type command
            for char in f"$ {cmd}\n":
                f.write(json.dumps([round(curr_time, 4), "o", char]) + "\n")
                curr_time += 0.05
            # Mock output
            output = f"Executing {cmd}...\nDone.\n"
            for char in output:
                f.write(json.dumps([round(curr_time, 4), "o", char]) + "\n")
                curr_time += 0.02
            curr_time += 0.5

def get_real_history(limit=10):
    try:
        # Try to get some real history but filter it
        hist_file = os.path.expanduser("~/.bash_history")
        if not os.path.exists(hist_file):
            hist_file = os.path.expanduser("~/.zsh_history")
            
        if os.path.exists(hist_file):
            with open(hist_file, 'r', errors='ignore') as f:
                lines = f.readlines()
                # Clean and filter (no keys, no secrets)
                clean = []
                for l in reversed(lines):
                    l = l.strip()
                    if not l or any(x in l.lower() for x in ["key", "pass", "token", "secret", "sig"]):
                        continue
                    clean.append(l)
                    if len(clean) >= limit:
                        break
                return clean
    except:
        pass
    return ["ls -la", "git status", "python3 --version", "cat README.md"]

if __name__ == "__main__":
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    history = get_real_history(limit=limit)
    
    target = sys.argv[1] if len(sys.argv) > 1 else "/home/citrullin/git/sovereign_stack_vision/docs/a2a_telemetry/mock_session.cast"
    
    os.makedirs(os.path.dirname(target), exist_ok=True)
    generate_mock_asciinema(history, target)
    print(f"[GENESIS] Generated mock asciinema trace: {target}")
