#!/usr/bin/env bash
# Run the A2A trace recorder inside a podman container
REPO_PATH="/home/citrullin/git/sovereign_stack_vision"

podman run --rm -it \
    -v "$REPO_PATH:/workspace:Z" \
    -w /workspace \
    --security-opt=no-new-privileges \
    docker.io/library/alpine:latest \
    sh -c "apk add --no-cache asciinema python3 && python3 tools/manifesto-scripts/start_a2a_trace.py $1"
