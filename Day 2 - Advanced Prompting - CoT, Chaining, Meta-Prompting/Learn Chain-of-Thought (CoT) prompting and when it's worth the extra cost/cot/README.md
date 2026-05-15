# Chain-of-Thought vs Self-Consistency Evaluation

This project evaluates different prompting techniques using Gemini models for insurance claim reasoning tasks.

The experiment compares:

1. Direct Prompting
2. Chain-of-Thought (CoT)
3. Self-Consistency (SC)

The goal is to measure:
- Accuracy
- Token usage
- Cost per technique
- Cost per correct answer

---

# Project Structure

```text
cot/
│
├── scenarios.jsonl
├── results.csv
├── cot_decision_rule.md
├── run_experiment.py
│
├── prompts/
│   ├── direct.txt
│   ├── cot.txt
│   └── sc.txt
│
└── README.md
```

---

# Concepts

## 1. Direct Prompting

The model answers immediately without explicit reasoning.

Example:

```text
Answer only Yes or No.

Scenario:
{scenario}
```

Advantages:
- Fast
- Cheap
- Low token usage

Disadvantages:
- Lower reasoning reliability for complex tasks

---

## 2. Chain-of-Thought (CoT)

The model is instructed to reason step-by-step before answering.

Example:

```text
Think step by step before answering.

Scenario:
{scenario}

Finally answer only Yes or No.
```

Advantages:
- Better reasoning
- More explainable
- Improved transparency

Disadvantages:
- Higher token usage
- More expensive

---

## 3. Self-Consistency (SC)

The CoT prompt is executed multiple times with higher temperature.

Process:
1. Run CoT prompt 5 times
2. Use temperature = 0.7
3. Take majority answer

Advantages:
- Most robust reasoning
- Reduces random reasoning failures

Disadvantages:
- 5x higher cost
- Slower execution

---

# Requirements

Install dependencies:

```bash
pip install google-genai python-dotenv pandas
```

---

# Environment Variables

Create a `.env` file:

```env
PROJECT_ID=your_project_id
LOCATION=us-central1
MODEL_NAME=gemini-2.5-flash
```

Authentication:

```bash
gcloud auth application-default login
```

---

# Running the Experiment

Execute:

```bash
python run_experiment.py
```

The script will:
1. Load scenarios
2. Run Direct Prompting
3. Run CoT Prompting
4. Run Self-Consistency
5. Calculate token cost
6. Export results

---

# Pricing Logic

The script calculates cost using token usage metadata.

Example pricing:

```python
INPUT_PRICE_PER_1M = 0.35
OUTPUT_PRICE_PER_1M = 1.05
```

Cost Formula:

```python
cost =
(input_tokens / 1_000_000 * input_price)
+
(output_tokens / 1_000_000 * output_price)
```

---

# Output Files

## 1. scenarios.jsonl

Contains all reasoning scenarios.

Example:

```json
{
  "scenario_id": 1,
  "scenario": "...",
  "ground_truth": "Yes"
}
```

---

## 2. results.csv

Contains:
- answers
- correctness
- token cost

Columns:

```text
scenario_id
direct_answer
direct_correct
cot_answer
cot_correct
sc_answer
sc_correct
direct_cost_usd
cot_cost_usd
sc_cost_usd
```

---

## 3. cot_decision_rule.md

Contains:
- accuracy comparison
- cost analysis
- cost per correct answer
- final decision rules

---

# Example Console Output

```text
============================================================
Scenario 1
============================================================

Running DIRECT prompting...
Direct Answer: No
Direct Cost: $1.575e-05

Running CoT prompting...
CoT Answer: No
CoT Cost: $0.0001386

Running Self-Consistency...
SC Run 1/5
SC Run 2/5
SC Run 3/5
SC Run 4/5
SC Run 5/5

Majority Answer: No
SC Total Cost: $0.00068355
```

---

# Key Findings

Typical observations:

| Technique | Accuracy | Cost |
|---|---|---|
| Direct | Lowest reasoning capability | Cheapest |
| CoT | Better reasoning | Moderate |
| Self-Consistency | Best robustness | Most expensive |

---

# Decision Rules

## Use Direct Prompting When:
- Tasks are simple
- Speed matters
- Cost matters

---

## Use CoT When:
- Multi-step reasoning is needed
- Explainability matters
- Business logic validation is required

---

## Use Self-Consistency When:
- Accuracy is critical
- Reasoning is ambiguous
- Small errors are expensive

Examples:
- legal reasoning
- healthcare
- fraud detection
- financial risk systems

---

# Reference

- https://www.promptingguide.ai/techniques/cot
- Gemini API Documentation
- Vertex AI Generative AI SDK

---

# Author

Chain-of-Thought Evaluation Project using Gemini + Vertex AI