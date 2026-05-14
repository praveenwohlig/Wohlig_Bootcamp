# Structured Invoice Extraction using Gemini + Pydantic

## Overview

This project demonstrates enterprise-style document extraction using:

- Gemini Multimodal (Vertex AI)
- Structured Outputs (`response_schema`)
- Pydantic schema validation
- PDF invoice extraction
- Field-level accuracy evaluation

The system extracts structured JSON from invoice PDFs using Gemini and validates the output against a predefined Pydantic schema.

This workflow is similar to real-world:
- Accounts Payable automation
- ERP ingestion pipelines
- Intelligent Document Processing (IDP)
- Invoice AI extraction systems

---

# Project Structure

```text
extractor/
│
├── .env
├── requirements.txt
├── README.md
├── main.py
├── schema.py
├── ground_truth.jsonl
├── field_accuracy.csv
├── accuracy_summary.md
│
└── samples/
    ├── invoice_1.pdf
    ├── invoice_2.pdf
    ├── invoice_3.pdf
    ├── invoice_4.pdf
    ├── invoice_5.pdf
    ├── invoice_6.pdf
    ├── invoice_7.pdf
    ├── invoice_8.pdf
    ├── invoice_9.pdf
    └── invoice_10.pdf
```

---

# Features

- Multimodal PDF invoice extraction
- Structured JSON outputs
- Pydantic validation
- Nested schema support
- Enum field handling
- Line item extraction
- Type-safe extraction pipeline
- Field-level benchmarking
- Ground-truth comparison

---

# Technologies Used

- Python
- Vertex AI Gemini
- Google GenAI SDK
- Pydantic
- response_schema
- Multimodal PDF processing

---

# Setup Instructions

## 1. Create Virtual Environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
PROJECT_ID=your-gcp-project-id
LOCATION=us-central1
MODEL_NAME=gemini-2.5-flash
```

---

# Vertex AI Authentication

Authenticate with Google Cloud:

```bash
gcloud auth application-default login
```

---

# Run Extraction

Run extraction on a single invoice PDF:

```bash
python3 main.py samples/invoice_1.pdf
```

---

# Run All Samples

macOS/Linux:

```bash
for file in samples/*.pdf; do
  python3 main.py "$file"
done
```

---

# Evaluation

The extracted JSON outputs were compared against manually created ground-truth JSON files.

Evaluation includes:
- field-level exact match comparison
- nested object validation
- line item validation
- enum normalization checking

---

# Enterprise Relevance

This architecture is similar to systems used for:
- invoice processing
- KYC extraction
- insurance claims
- ERP automation
- financial document intelligence
- enterprise OCR workflows

---

# Reference

https://ai.google.dev/gemini-api/docs/structured-output
