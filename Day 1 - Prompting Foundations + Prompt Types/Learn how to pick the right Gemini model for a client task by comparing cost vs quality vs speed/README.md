# README - Gemini Model Benchmarking & Evaluation

## Overview

This project benchmarks multiple Gemini models on document summarization tasks.

The script:
- Reads `.txt` files from the `inputs/` directory
- Sends each document to multiple Gemini models
- Measures:
  - latency
  - token usage
  - estimated cost
  - summary quality
- Uses Gemini-as-a-Judge for automated evaluation
- Saves all benchmark results into a CSV file

---

# Features

- Multi-model benchmarking
- Latency measurement
- Token usage tracking
- Cost estimation
- Gemini-as-a-Judge evaluation
- CSV export
- Automated document processing

---

# Models Used

| Model | Purpose |
|---|---|
| gemini-3.1-pro-preview | High-quality reasoning |
| gemini-2.5-flash | Fast balanced generation |
| gemini-2.5-flash-lite | Low-cost lightweight generation |
| gemini-2.5-pro | Judge/Evaluator |

---

# Project Structure

```text
project/
│
├── benchmark.py
├── results.csv
├── README.md
│
└── inputs/
    ├── doc1.txt
    ├── doc2.txt
    └── doc3.txt
```

---

# Setup Instructions

## 1. Create Virtual Environment

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

# 2. Install Dependencies

```bash
pip install google-genai
```

---

# 3. Authenticate Vertex AI

Login using Google Cloud CLI:

```bash
gcloud auth application-default login
```

---

# 4. Configure Project

Update the script with your Vertex AI project details:

```python
client = genai.Client(
    vertexai=True,
    project="your-project-id",
    location="global"
)
```

---

# Input Documents

Place all `.txt` files inside the `inputs/` directory.

Example:

```text
inputs/
├── invoice.txt
├── report.txt
└── contract.txt
```

---

# Running the Benchmark

Run the script:

```bash
python3 run.py
```

---

# What the Script Does

For every input file:
1. Sends the document to all configured Gemini models
2. Generates a summary
3. Measures latency
4. Tracks token usage
5. Calculates estimated cost
6. Uses Gemini-as-a-Judge for quality evaluation
7. Saves results to CSV

---

# Output CSV

Results are saved into:

```text
results.csv
```

---

# CSV Columns

| Column | Description |
|---|---|
| input_id | Input filename |
| model | Gemini model used |
| latency_ms | Response latency in milliseconds |
| input_tokens | Prompt token count |
| output_tokens | Generated token count |
| cost_usd | Estimated cost |
| quality_score_1to5 | Judge quality score |
| notes | Judge feedback |

---

# Example Output

| input_id | model | latency_ms | quality_score_1to5 |
|---|---|---|---|
| invoice | gemini-2.5-flash | 1450 | 5 |
| report | gemini-2.5-flash-lite | 820 | 4 |

---

# Example Console Output

```text
Processing: report.txt

Done: report | gemini-3.1-pro-preview
Done: report | gemini-2.5-flash
Done: report | gemini-2.5-flash-lite

Completed Successfully
```

---

# Cost Calculation

The script estimates cost using:
- input token pricing
- output token pricing

Cost is calculated per 1 million tokens.

---

# Gemini-as-a-Judge

The evaluation model:
- rates summary quality from 1–5
- checks:
  - accuracy
  - clarity
  - completeness
- returns a short evaluation note

Judge model used:

```text
gemini-2.5-pro
```

---

# Example Evaluation

```text
Score: 5
Note: Accurate and concise summary
```

---

# Future Improvements

Possible enhancements:
- parallel processing
- JSON evaluation outputs
- visualization dashboard
- benchmark charts
- hallucination scoring
- BLEU/ROUGE metrics
- retry handling
- async generation
- batch processing

---

# Conclusion

This project demonstrates:
- LLM benchmarking
- automated evaluation
- cost tracking
- performance analysis
- Gemini-as-a-Judge workflows
- enterprise GenAI evaluation pipelines

It provides a scalable framework for comparing Gemini models on real-world summarization tasks.
