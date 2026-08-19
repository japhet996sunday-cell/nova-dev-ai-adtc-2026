# ADTC 2026 — Nova Dev AI

**Nova Dev AI** is a privacy-first, offline coding assistant designed to help self-taught programmers and bootcamp learners understand, write, and debug code without requiring an internet connection during inference.

It combines a compact quantized **Qwen2.5-Coder-1.5B-Instruct** model with a local programming-fundamentals knowledge base and lightweight keyword-based retrieval.

---

## 🚀 Key Features

- Fully offline inference
- Privacy-first architecture
- Qwen2.5-Coder-1.5B-Instruct
- GGUF Q4_K_M quantization
- llama.cpp runtime
- Local RAG knowledge base
- No external API required during inference
- Designed for resource-constrained hardware
- Programming explanations and debugging assistance
- Local educational grounding for improved explanations

---

## 🧠 How Nova Dev AI Works

The assistant follows this pipeline:

```text
User Question
      ↓
Local RAG Retriever
      ↓
Relevant Knowledge Document
      ↓
Prompt Construction
      ↓
Qwen2.5-Coder-1.5B-Instruct
      ↓
Generated Coding Response
```

The retrieval component searches the local `knowledge/` corpus and selects relevant programming-fundamentals material using keyword overlap.

The selected document is then incorporated into the prompt sent to the local model.

This makes the RAG component load-bearing rather than decorative: retrieved knowledge changes the actual prompt received by the model.

---

## 📚 Cross-Disciplinary Component

Nova Dev AI uses **education** as its cross-disciplinary pairing.

The assistant is designed for self-taught developers and bootcamp learners who may need explanations of fundamental programming concepts in addition to code generation.

The local corpus contains programming fundamentals covering topics such as:

- Variables and data types
- Functions
- Loops and iteration
- Debugging
- Programming concepts
- Other foundational development topics

The knowledge base operates entirely locally and does not require a second embedding model or external retrieval service.

---

## 🤖 Model

| Property | Value |
|---|---|
| Model | Qwen2.5-Coder-1.5B-Instruct |
| Architecture | Qwen2 |
| Parameters | ~1.78B |
| Quantization | GGUF Q4_K_M |
| Runtime | llama.cpp |
| Context length | 32,768 |
| Packaging | Binary bundle |
| Inference | Offline |

The model weights are downloaded using the repository's model download script and are not committed directly to the repository.

---

## 🔒 Privacy and Offline Operation

Nova Dev AI is designed to operate without sending user code or prompts to external services during inference.

The inference pipeline consists of:

- Local model
- Local knowledge base
- Local retrieval
- Local prompt construction
- Local generation

No cloud LLM API is required for normal assistant operation.

---

## 📁 Repository Structure

```text
nova-dev-ai-adtc-submission/
│
├── metadata.json
├── submission.json
├── REPORT.md
├── README.md
├── download_model.sh
├── run_assistant.py
├── rag_retrieve.py
│
├── knowledge/
│   ├── functions.md
│   ├── variables-and-types.md
│   ├── loops-and-iteration.md
│   └── ...
│
├── model/
│   └── qwen2.5-coder-1.5b-instruct-q4_k_m.gguf
│
└── .github/
    └── workflows/
        └── ...
```

The GGUF model file is excluded from version control.

---

## ▶️ Running the Assistant

### 1. Clone the repository

```bash
git clone https://github.com/japhet996sunday-cell/nova-dev-ai-adtc-2026.git
cd nova-dev-ai-adtc-2026
```

### 2. Download the model

```bash
bash download_model.sh
```

The script downloads the required GGUF model into the `model/` directory.

### 3. Run the assistant

```bash
python run_assistant.py
```

The assistant can then process programming questions using the local model and knowledge base.

---

## 🧪 Example Questions

**Python debugging**
> How do I debug a Python function that returns the wrong value?

**Programming fundamentals**
> What is a Python function?

**Data structures**
> Why does a Python list index start at zero?

The RAG retriever selects relevant local educational material before the model generates the response.

---

## 🖥️ Development Environment Note

Development and local validation were performed using Android/Termux because it was the hardware environment available to the project. Termux was used to test the offline model runtime, repository tooling, model packaging, and reproducibility of the submission pipeline.

Because Android/Termux does not reproduce the competition's specified benchmark environment, the official performance figures reported for this submission were generated separately using the GitHub Actions benchmark runner configured for the project.

---

## 🧪 Functional Testing

The complete offline pipeline has been tested on an ARM64 Android/Termux development device.

The tested path was:

```text
User question
     ↓
RAG retrieval
     ↓
Prompt construction
     ↓
Qwen2.5-Coder model
     ↓
Generated response
     ↓
Clean process exit
```

Representative tests successfully verified:

- Python function explanation
- Python list/index explanation
- Python debugging
- Relevant local knowledge retrieval
- Successful model loading
- Successful response generation
- Clean process termination

A knowledge-base correction was also verified through the RAG retriever. The documentation correctly states that a Python function reaching the end without a return statement returns the Python value `None`.

---

## 📊 Benchmark Results

### Primary GitHub Actions Benchmark

The primary quantitative benchmark was obtained using the ADTC profiler in a GitHub Actions evaluation environment.

| Metric | Result |
|---|---|
| Model | Qwen2.5-Coder-1.5B-Instruct |
| Quantization | GGUF Q4_K_M |
| CPU | AMD EPYC 7763 64-Core Processor |
| RAM | 15.6 GB |
| GPU | None |
| OS | Ubuntu 24.04.4 LTS |
| Generation throughput | 28.83 tokens/s |
| First-token latency | 8460.38 ms |
| Peak RSS | 1828.18 MB |
| Steady-state RSS | 1782.57 MB |
| ARC-Easy accuracy | 64% |
| CPU p99 | 55.0% |
| CPU throttling | No |

**Calculated Performance**

Using the documented ADTC profiler formula:

```text
SPERF = min(TPS / TPS_REFERENCE, 1.0) × 100
```

With:
- TPS = 28.83
- TPS_REFERENCE = 15.0

The resulting calculated score is: **SPERF = 100.00**

**Calculated Efficiency**

Using:

```text
SEFF = max(0, (RAM_LIMIT_GB - peak_rss_gb) / RAM_LIMIT_GB) × 100
```

With:
- RAM_LIMIT_GB = 7.0
- Peak RSS = 1828.18 MiB = 1.7853 GiB

The resulting calculated score is: **SEFF = 74.50**

**Derived Weighted Score**

Using:

```text
0.50 × S_acc + 0.30 × S_perf + 0.20 × S_eff
```

With:
- Accuracy = 64.00
- SPERF = 100.00
- SEFF = 74.50

The resulting derived weighted score is: **76.90 / 100**

These are calculated values based on the recorded benchmark measurements and documented formulas. They should not be described as an independently issued official leaderboard score unless the ADTC platform publishes that score.

### Historical GitHub Actions Benchmark

An earlier GitHub Actions benchmark is retained as historical reproducibility evidence. It was measured on different CI runner hardware and is therefore reported separately.

| Metric | Historical Result |
|---|---|
| CPU | Intel Xeon Platinum 8573C |
| Generation throughput | 17.13 tokens/s |
| First-token latency | 2528.18 ms |
| Peak RSS | 2000.65 MB |
| Steady-state RSS | 1919.82 MB |
| ARC-Easy accuracy | 68% |
| CPU p99 | 52.8% |
| Peak temperature | 49.9°C |
| CPU throttling | No |

The two GitHub Actions runs are not averaged because the runner hardware was different.

---

## 📱 Android/Termux Development Evidence

Additional development testing was performed on an ARM64 Android/Termux device. These results are supplementary development evidence and are not used as the official ADTC benchmark.

### Concurrent Process Testing

Two independent assistant processes were launched concurrently.

**Result: 2/2 processes completed successfully.**

The processes successfully:
- Loaded the model
- Retrieved local knowledge
- Generated responses
- Exited cleanly
- Returned exit code 0

A four-process concurrent test was also performed.

**Result: 0/4 processes completed successfully.**

This exceeded the practical resource capacity of the Android/Termux development configuration and is treated as a development-device resource limitation rather than a failure of the normal single-process pipeline.

### Android llama-bench

A completed Android/Termux llama-bench measurement recorded:

| Configuration | Prompt Processing | Generation | Threads | Result |
|---|---|---|---|---|
| pp64 / tg16 | 1.70 tokens/s | 0.14 tokens/s | 4 | PASS |
| pp128 / tg128 | 3.70 tokens/s | Not completed | 8 | INTERRUPTED |

The completed measurement used the packaged Qwen2.5-Coder-1.5B-Instruct Q4_K_M model.

The Android runtime also reported:

```text
ggml_vulkan: No devices found.
```

This is a device-specific Android/Termux observation and does not represent the official ADTC evaluation runtime.

The Android measurements are deliberately kept separate from the GitHub Actions benchmark. They are not used to calculate:
- Official SPERF
- Official SEFF
- Official accuracy
- Official memory score
- Official thermal score
- Official weighted score

---

## 🔬 Reproducibility

Primary benchmark reproducibility information:

| Property | Value |
|---|---|
| Git commit | 5f358209a482 |
| Random seed | 42 |
| Architecture | qwen2 |
| Parameters measured | 1,777,088,000 |
| Context length | 32768 |
| Runtime | llama.cpp |
| Quantization | GGUF Q4_K_M |
| Accuracy benchmark | ARC-Easy |
| Accuracy samples | 50 |

The model is obtained through the repository download mechanism rather than committed as a large GGUF weight file.

---

## 📈 Benchmark Summary

| Environment | Purpose | Generation | Accuracy | Peak RSS | Status |
|---|---|---|---|---|---|
| GitHub Actions — Primary | Primary ADTC benchmark | 28.83 tok/s | 64% | 1828.18 MB | Primary |
| GitHub Actions — Historical | Reproducibility | 17.13 tok/s | 68% | 2000.65 MB | Historical |
| Android/Termux | Development evidence | 0.14 tok/s (tg16) | Not official | Not used | Supplementary |

### Primary Derived Scores

| Score | Result |
|---|---|
| SPERF | 100.00 |
| SEFF | 74.50 |
| Derived weighted score | 76.90 / 100 |

The GitHub Actions result is the primary quantitative benchmark. Android/Termux measurements are included only as supplementary evidence of offline operation and development testing.

---

## 🏁 Submission Checklist

Before submission:

- [x] Public GitHub repository
- [x] metadata.json completed
- [x] Exactly two test prompts provided
- [x] GGUF model download mechanism provided
- [x] GGUF model excluded from Git
- [x] REPORT.md completed
- [x] Offline inference supported
- [x] Local RAG knowledge base included
- [x] Functional pipeline tested
- [x] GitHub Actions benchmark completed
- [x] Historical benchmark retained separately
- [x] Android/Termux development evidence documented
- [x] submission.json generated by the ADTC profiler

---

## 👤 Team

**Team:** Nova Dev AI
**Domain:** Coding Assistants
**Submitter:** Japhet Sunday
**GitHub:** [japhet996sunday-cell](https://github.com/japhet996sunday-cell)

Nova Dev AI focuses on making useful coding assistance available locally and privately, particularly for learners and developers working with limited hardware or unreliable internet connectivity.
