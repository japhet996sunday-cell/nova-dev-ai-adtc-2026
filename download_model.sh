#!/usr/bin/env bash
# Download the model weight file for this submission.
#
# Rules (per the official ADTC 2026 submission template):
#   - Must be idempotent (safe to run multiple times).
#   - Must download without any credentials (public URL only).
#   - The output path must match `_runtime.model_path` in metadata.json.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL_DIR="$HERE/model"
MODEL_FILE="$MODEL_DIR/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"

# ── Verified public URL — Qwen's own official GGUF release ─────────────────────
# Source: https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF
# License: Apache-2.0. Confirmed file size at time of writing: 491 MB.
MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF/resolve/main/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
# ───────────────────────────────────────────────────────────────────────────────

mkdir -p "$MODEL_DIR"

if [[ -f "$MODEL_FILE" ]]; then
  echo "model already present at $MODEL_FILE — skipping download"
  exit 0
fi

echo "downloading $MODEL_URL -> $MODEL_FILE (~491 MB)..."

if command -v curl > /dev/null 2>&1; then
  curl -L --fail --progress-bar -o "$MODEL_FILE.partial" "$MODEL_URL"
elif command -v wget > /dev/null 2>&1; then
  wget --show-progress -O "$MODEL_FILE.partial" "$MODEL_URL"
else
  echo "error: neither curl nor wget found" >&2
  exit 1
fi

mv "$MODEL_FILE.partial" "$MODEL_FILE"
echo "done: $MODEL_FILE"
echo ""
echo "NOTE: this download has not been executed in the environment that"
echo "authored this script (no huggingface.co network access there.)"
echo "The URL above was verified by fetching the model's real file listing"
echo "page (confirmed present, 491 MB) but the download itself, and every"
echo "step after it (llama-bench, adtc-profiler), must be run locally."
echo "See REPORT.md's Verification section."
