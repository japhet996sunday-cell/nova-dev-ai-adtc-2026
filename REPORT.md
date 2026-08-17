# Technical Report — Nova Dev AI (llama.cpp / GGUF submission)

**Team ID:** nova-dev-ai
**Domain:** coding_assistants
**Model:** Qwen2.5-Coder-1.5B-Instruct-Q4_K_M

---

## Problem

Cloud-hosted coding assistants assume a stable, generous internet connection and a willingness to pay a recurring per-token or per-seat cost. For self-taught developers, bootcamp learners, and junior developers on modest hardware and metered or intermittent connectivity, that assumption is a real barrier, not a minor inconvenience.

This submission is a coding assistant that runs entirely on-device via llama.cpp against a quantized GGUF model, targeting the ADTC Standard Laptop (8 GB RAM, integrated graphics, no discrete GPU). After the one-time 1.1 GB model download, it needs no network connection to generate code, explain concepts, or help debug — which matters directly for a student in Lagos, Nairobi, or Kampala working through unreliable or expensive connectivity, and matters generally for anyone who wants their code and questions to stay on their own machine.

## Design Decisions

**Base model:** Qwen2.5-Coder-1.5B-Instruct, from Qwen's own official GGUF release (`Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF` on Hugging Face, Apache-2.0 licensed). Qwen2.5-Coder is a code-specialized model family (not a general-purpose model repurposed for code), so at a given parameter count it should outperform a general model on the coding-tutoring/debugging/generation tasks this domain actually asks for.

**Quantization:** Q4_K_M — 1.1 GB on disk. This is the same quantization level the official submission template itself uses in its own worked example (SmolLM2-135M-Instruct-Q4_K_M), and is a well-established balance point: noticeably smaller than Q8_0 (676 MB) or fp16 (1.27 GB) with modest quality loss relative to those, and better quality than the more aggressive Q2_K/Q3_K_M tiers.

**Size (1.5B parameters):** This submission deliberately does not reach for the largest model that might technically fit in the 7 GB budget. The 8 GB target machine is integrated-graphics-only, so the entire model, the KV cache, and llama.cpp's own working memory all compete for the same shared system RAM as the OS and everything else running on the judge's sandboxed evaluation environment (documented as 8 GB RAM / 4 CPU cores). A small model that loads reliably, generates without paging, and stays far from the 7 GB disqualification ceiling is a safer, more defensible engineering choice than a larger model that might score higher on accuracy in principle but risks an OOM disqualification (`S_total = 0`) in practice. Larger Qwen2.5-Coder tiers (1.5B, 3B, 7B) exist and would very likely score higher on `S_acc` if headroom allows — see "Alternatives considered."

**Alternatives considered:**
- **Qwen2.5-Coder-0.5B-Instruct-GGUF:** considered for its smaller memory footprint, but the 1.5B model was selected because it provides substantially more model capacity while still being practical to test locally.
- **Qwen2.5-Coder-3B/7B:** potentially stronger on accuracy, but larger models require substantially more memory and introduce greater risk against the 7 GB peak-RAM disqualification ceiling.
- **A larger general-purpose model (e.g. Llama 3.2 3B) instead of a code-specialized one:** rejected because Qwen2.5-Coder is specifically trained for code generation, reasoning, and fixing, which directly matches the coding-assistant domain.
- **An embeddings-based RAG retriever:** rejected in favor of stdlib-only keyword-overlap scoring to avoid adding a second model and its RAM footprint.


## Constraints

- Target: 8 GB RAM, integrated GPU, Ubuntu 22.04 — no GPU acceleration, pure CPU inference via llama.cpp.
- **7 GB is a hard ceiling, not a soft penalty** — per the official challenge site, exceeding it is immediate disqualification (`S_total = 0`), which shaped the model-size decision above more than the accuracy/throughput trade-off did.
- Zero network dependency during evaluation — the model must run 100% offline once `download_model.sh` has completed.
- No parameter-count/file-size cap is imposed by the rules, but `llama.cpp`/GGUF is the *only* supported runtime; this submission does not use WebLLM, WebGPU, or MLC-format weights anywhere in this directory (see "Relationship to Nova Dev AI" below for where those *are* used, and why that's a separate layer).

## Cross-Disciplinary Integration

**Pairing: Coding Assistant × Programming Education.** `knowledge/*.md` is a small, curated local corpus (debugging strategy, variables/types, functions, loops, and working offline) written for the same self-taught/bootcamp-learner audience the coding-assistant domain already targets. `rag_retrieve.py` scores the corpus by keyword overlap with the user's question (stdlib-only, no embeddings model, sub-millisecond) and `run_assistant.py` prepends the best match to the prompt actually sent to llama.cpp. This is load-bearing — it changes model input and therefore output — not a description-only claim. See `metadata.json`'s `cross_disciplinary_pairing` block.


## Relationship to Nova Dev AI (the broader product)

This directory is deliberately separate from the main Nova Dev AI repository, which is a polished PWA built around WebLLM/WebGPU (browser-based, MLC-format weights). That separation is intentional, not an oversight: the official evaluation pipeline runs `llama-bench`/`adtc-profiler` against a GGUF file per this template's structure and explicitly does not measure a broader application UI or stack. WebLLM is not a supported runtime for this competition's automated evaluation ("llama.cpp only," per the official FAQ). The WebLLM-based application remains valuable as the product/demo layer — the polished chat UX, conversation history, and coding-mode system prompts it implements are real and reused conceptually here (the same Qwen2.5-Coder model family, the same target hardware assumptions) — but it is not, and is no longer documented as, the artifact this competition scores.

## Benchmarks

### Android/Termux development-device measurements

Real `llama-bench` measurements were obtained on the author's ARM64 Android/Termux development device using the packaged Qwen2.5-Coder-1.5B-Instruct Q4_K_M GGUF model.

These are **real development-device measurements, not official ADTC benchmark scores**. The competition's official performance, efficiency, memory, thermal, and accuracy measurements remain authoritative.

| Configuration | Prompt processing | Text generation | Threads | Result |
|---|---:|---:|---:|---|
| `pp64 / tg16` | **1.70 t/s** | **0.14 t/s** | 4 | PASS |
| `pp128 / tg128` | **3.70 t/s** | Not completed | 8 | INTERRUPTED |

#### Completed benchmark: pp64 / tg16

The completed `llama-bench` run reported:

- Model: Qwen2.5-Coder 1.5B Q4_K_M
- Model size: **1.04 GiB**
- Parameters reported by llama-bench: **1.78 B**
- Backend reported by llama-bench: **Vulkan**
- Threads: **4**
- Prompt processing (`pp64`): **1.70 tokens/second**
- Text generation (`tg16`): **0.14 tokens/second**
- Repetitions: **1**
- Build: `unknown (0)`
- Result: **PASS — benchmark completed**

The Termux runtime also reported `ggml_vulkan: No devices found.` before loading the Vulkan and CPU backends. This is a device-specific Android/Termux observation and should not be interpreted as the official competition runtime configuration.

### Official benchmark status

The Android/Termux measurements above are useful development-device evidence, but they are **not substitutes for the official ADTC evaluation**. In particular, they do not establish the official peak RAM, thermal score, efficiency score, or normalized performance score.

The official profiler remains the authoritative way to obtain those values on a compatible evaluation environment.
## Functional Pipeline Testing

The core assistant/RAG pipeline was functionally tested on an ARM64 Android/Termux development device using the packaged Qwen2.5-Coder-1.5B-Instruct Q4_K_M GGUF model and `run_assistant.py`.

The tests verify the complete path:

**User question → RAG retrieval → prompt construction → Qwen2.5-Coder model → generated answer → clean process exit**

### Functional test results

| Test | Question | Retrieved knowledge | Result |
|---|---|---|---|
| 1 | `What is a Python function?` | `functions.md` | PASS |
| 2 | `Why does a Python list index start at zero?` | `loops-and-iteration.md` | PASS |
| 3 | `How do I debug a Python function that returns the wrong value?` | `functions.md` | PASS |

### Observations

- The model loaded successfully for all three tests.
- The RAG retriever selected relevant local knowledge documents for each query.
- Retrieved material was visibly incorporated into the generated prompt.
- The model produced usable answers for all three questions.
- The assistant exited automatically after each single-turn request.
- No Python traceback, model-load failure, RAG failure, or hanging process occurred during these three functional tests.
- These tests demonstrate functional operation of the core offline assistant/RAG pipeline. They are not intended to represent the official ADTC benchmark performance, which must be measured against the competition's standardized evaluation environment.

### Knowledge-base quality note

During functional testing, `functions.md` was found to contain an incorrect "`None` or `undefined`" wording. This was corrected so the knowledge base now correctly states that a Python function with no returned value falls through and returns `None`. The correction was verified with the RAG retriever after editing the knowledge base.

## Concurrent Functional Testing

Additional concurrency testing was performed on the ARM64 Android/Termux development device using the packaged Qwen2.5-Coder-1.5B-Instruct Q4_K_M GGUF model.

These tests launched separate `run_assistant.py` processes concurrently. They are therefore described as **concurrent processes**, not threads, because each process loads its own model/runtime instance.

### 2-process concurrent test

Two assistant processes were launched simultaneously:

1. `What is a Python variable?`
2. `What is a Python function?`

Both processes:

- loaded the Qwen2.5-Coder model successfully;
- retrieved relevant local knowledge (`variables-and-types.md` and `functions.md`);
- generated responses;
- reached a clean `Exiting...` state;
- returned exit code `0`.

**Result: 2/2 processes completed successfully.**

The test took approximately **545.8 seconds of wall-clock time** on the Android/Termux development device. This is a development-device performance observation and is not an official competition benchmark.

The initial test harness reported `FAIL/CHECK` because its output-marker check was too strict for concurrently buffered/interleaved output. Manual inspection confirmed successful model loading, RAG retrieval, generation, clean exit, and exit code `0` for both processes.

### 4-process concurrent test

Four assistant processes were launched simultaneously using the following questions:

1. `What is a Python variable?`
2. `What is a Python function?`
3. `Why does a Python list index start at zero?`
4. `How do I debug a Python function that returns the wrong value?`

All four processes exited with code **247** before completing the normal assistant pipeline.

**Result: 0/4 completed successfully.**

This indicates that running four independent model instances concurrently exceeds the practical resource capacity of the development device/runtime configuration. It should not be interpreted as a failure of the single-process assistant pipeline.

### Concurrency conclusion

The assistant's core pipeline is functional in single-process operation and successfully completed a two-process concurrent test. Four simultaneous model instances were not sustainable on the ARM64 development device and resulted in exit code 247.

Because the official ADTC evaluation targets a standard 8 GB RAM laptop and evaluates the submitted model/runtime under its own controlled conditions, these Android concurrency results are development-device observations rather than official ADTC benchmark results.
