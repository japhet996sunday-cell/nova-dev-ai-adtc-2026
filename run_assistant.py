#!/usr/bin/env python3
"""
run_assistant.py — Nova Dev AI coding assistant, local RAG + llama.cpp.

    python3 run_assistant.py "Why does my loop skip the last element?"

Pipeline:
    user prompt -> rag_retrieve.py (local corpus lookup)
                -> prompt assembly (system + retrieved context + user prompt)
                -> llama-cli subprocess against the GGUF model
                -> generated response printed to stdout

NOT EXECUTED IN THIS ENVIRONMENT: this script has been written against the
documented, long-stable llama.cpp CLI flags (-m, -p, -n, --temp, -no-cnv)
and syntax-checked, but has not been run against a real model in this
sandbox — no llama-cli binary and no downloaded GGUF file are available
here (see REPORT.md "Verification" section). Before relying on it, confirm
your installed llama.cpp version's exact flags with `llama-cli --help`;
CLI flag names have changed across llama.cpp releases in the past.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from rag_retrieve import retrieve

HERE = Path(__file__).parent
DEFAULT_MODEL_PATH = HERE / "model" / "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"

SYSTEM_PROMPT = (
    "You are Nova, an offline coding assistant for students and developers "
    "learning to program, often with limited or unreliable internet access. "
    "Be concise, correct, and encourage good debugging habits. Treat the retrieved reference material as authoritative. Do not contradict it. Check technical claims before answering, especially error types, syntax, indexing, and code behavior."
)


def build_prompt(user_query: str) -> str:
    """Assembles system + retrieved local context + user query into one prompt."""
    parts = [SYSTEM_PROMPT]

    matches = retrieve(user_query, top_k=1)
    if matches:
        parts.append(
            "Relevant reference material from the local knowledge base "
            f"({matches[0]['source']}):\n{matches[0]['content']}"
        )

    parts.append(f"User question: {user_query}")
    return "\n\n".join(parts)


def find_llama_cli() -> str | None:
    """Looks for llama-cli (current name) or the older `main` binary on PATH."""
    return shutil.which("llama-cli") or shutil.which("main")


def run(user_query: str, model_path: Path, n_predict: int = 128, temp: float = 0.2) -> int:
    binary = find_llama_cli()
    if binary is None:
        print(
            "error: llama-cli not found on PATH. Install llama.cpp and ensure "
            "llama-cli (or the legacy `main` binary) is available.\n"
            "See: https://github.com/ggerganov/llama.cpp",
            file=sys.stderr,
        )
        return 2

    if not model_path.exists():
        print(
            f"error: model file not found at {model_path}.\n"
            f"Run download_model.sh first.",
            file=sys.stderr,
        )
        return 2

    prompt = build_prompt(user_query)

    cmd = [
        binary,
        "-m", str(model_path),
        "-p", prompt,
        "-n", str(n_predict),
        "-t", "4",
        "-tb", "4",
        "--temp", str(temp),
        "-no-cnv",
        "-st",  # single turn; exit after the supplied prompt is completed
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"llama-cli exited with code {result.returncode}:\n{result.stderr}", file=sys.stderr)
        return result.returncode

    print(result.stdout)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Nova Dev AI — local coding assistant (llama.cpp)")
    parser.add_argument("prompt", nargs="+", help="Your coding question")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL_PATH, help="Path to the GGUF model file")
    parser.add_argument("--n-predict", type=int, default=512, help="Max tokens to generate")
    parser.add_argument("--temp", type=float, default=0.2, help="Sampling temperature")
    args = parser.parse_args()

    return run(" ".join(args.prompt), args.model, args.n_predict, args.temp)


if __name__ == "__main__":
    sys.exit(main())
