#!/bin/bash

set -euo pipefail

# start server in background
ollama serve &
OLLAMA_PID=$!

# wait for API to be ready
until curl -sf http://localhost:11434/ >/dev/null; do
  echo "Waiting for Ollama..."
  sleep 1
done

# pull model if missing
MODEL_NAME="tinyllama"
if ! ollama list | grep -q "^${MODEL_NAME}"; then
  echo "Pulling ${MODEL_NAME}..."
  ollama pull ${MODEL_NAME}
fi

# bring server to foreground (replace shell)
wait $OLLAMA_PID
