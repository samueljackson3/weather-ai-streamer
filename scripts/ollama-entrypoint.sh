#!/bin/bash
set -e

echo "[startup] Starting Ollama server..."
/bin/ollama serve &
SERVER_PID=$!

echo "[startup] Waiting for Ollama server to be ready..."
until ollama list >/dev/null 2>&1; do sleep 1; done

echo "[startup] Pulling tinyllama..."
ollama pull tinyllama

echo "[startup] Model ready. Handing off to server process."
wait $SERVER_PID
