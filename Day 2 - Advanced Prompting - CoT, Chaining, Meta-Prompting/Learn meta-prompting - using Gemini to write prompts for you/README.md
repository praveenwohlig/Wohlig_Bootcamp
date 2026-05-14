# Meta Prompting with Gemini - README

## Goal

Learn meta-prompting by using Gemini to automatically generate high-quality prompts from vague business requests.

---

# Concept

A meta-prompt is a prompt that generates other prompts.

The system takes a vague request like:

```text
extract data from PDFs
```

and automatically generates a structured production-ready prompt containing:
- Role
- Context
- Task
- Constraints
- Format
- Examples

---

# Deliverables

1. `/meta/meta_prompt.txt`
2. `/meta/meta_prompter.py`
3. `/meta/test_briefs.md`
4. `/meta/generated_prompts/`
5. `/meta/judge_scorecard.csv`
6. `/meta/findings.md`

---

# Project Structure

```text
meta/
│
├── .env
├── meta_prompt.txt
├── meta_prompter.py
├── test_briefs.md
├── judge_scorecard.csv
├── findings.md
├── README.md
│
└── generated_prompts/
    ├── brief_1.md
    ├── brief_2.md
    ├── brief_3.md
    ├── brief_4.md
    └── brief_5.md
```

---

# Technologies Used

- Python
- Vertex AI
- Gemini 2.5 Flash
- Gemini 2.5 Pro
- python-dotenv
- argparse
- CSV / JSON processing

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

## 2. Install Dependencies

```bash
pip install google-genai python-dotenv
```

---

## 3. Configure Environment Variables

Create a `.env` file:

```env
PROJECT_ID=your-project-id
LOCATION=global
MODEL_NAME=gemini-2.5-flash
```

---

## 4. Authenticate Vertex AI

```bash
gcloud auth application-default login
```

---

# Running the Meta Prompter

## Example 1

```bash
python3 meta_prompter.py "extract data from PDFs"
```

## Example 2

```bash
python3 meta_prompter.py "classify support emails" --id brief_2
```

---

# Meta Prompting Workflow

```text
Vague Brief
    ↓
Meta Prompt
    ↓
Gemini Generates Structured Prompt
    ↓
Gemini Judge Evaluates Prompt
    ↓
JSON Evaluation
    ↓
CSV Scorecard
```

---

# Test Briefs Used

1. extract data from PDFs
2. classify support emails
3. write product descriptions
4. summarize legal documents
5. translate marketing copy

---

# Judge Evaluation

Judge model used:

```text
gemini-2.5-pro
```

Judge checks:
- all 6 required sections
- prompt quality
- clarity
- formatting
- production readiness

Expected JSON response:

```json
{
  "quality_score": 5,
  "has_all_6_sections": true,
  "what_was_missing": "None"
}
```

---

# Output Files

## Generated Prompts

Saved inside:

```text
generated_prompts/
```

## Judge Scorecard

Saved as:

```text
judge_scorecard.csv
```

Columns:
- brief_id
- generated_prompt_quality_1to5
- has_all_6_sections
- what_was_missing

---

# Findings

Documented in:

```text
findings.md
```

Includes:
- when meta-prompting is useful
- when manual prompting is faster
- tradeoffs between automation and customization

---

# Conclusion

This project demonstrates:
- Meta Prompting
- Gemini-as-a-Judge
- Automated Prompt Engineering
- Vertex AI Integration
- Enterprise GenAI workflows

The system converts vague business requests into structured production-ready prompts automatically using Gemini and Vertex AI.
