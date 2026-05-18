# Structured Output Self-Repair Evaluation

## Objective

Evaluate whether retry-based self-repair improves structured extraction reliability using Gemini 2.5 Flash and Pydantic validation.

The system used:
- Gemini 2.5 Flash
- response_schema structured outputs
- Pydantic validation
- Automatic retry/self-repair loop

---

# Dataset

Total Inputs Tested: 20

The dataset included:
- OCR corrupted business cards
- Invalid emails
- Broken phone numbers
- Mixed formatting
- Unicode/symbol noise
- Missing separators
- Garbled text
- OCR character substitutions

---

# Results Summary

| Metric | Without Repair | With Repair |
|---|---|---|
| Total Inputs | 20 | 20 |
| First Try Success | 8 | 8 |
| Retry Recovery | 0 | 12 |
| Final Success | 8 | 20 |
| Total Failures | 12 | 0 |
| Success Rate | 40% | 100% |

---

# Retry Analysis

| Retry Count | Number of Inputs |
|---|---|
| 0 Retries | 8 |
| 1 Retry | 8 |
| 2 Retries | 4 |
| 3 Retries | 0 |

Most extraction failures were successfully repaired within 1 retry.

---

# Common Errors Fixed

## 1. Invalid Email Formatting

Examples:
- `gmial.con`
- `gmail,com`
- `@@gmail.com`

The retry loop corrected malformed email structures successfully.

---

## 2. Phone Number Validation Errors

Examples:
- Alphabetic characters inside phone numbers
- OCR substitutions (`O → 0`)
- Incorrect digit counts

The repair loop fixed formatting and normalization issues.

---

## 3. Invalid JSON Structure

Examples:
- Missing nested address object
- Incorrect field types
- Malformed JSON formatting

Gemini corrected the schema after receiving validation feedback.

---

## 4. Pincode Validation Issues

Examples:
- Non-digit characters
- Incorrect lengths
- OCR corruption

The retry prompts improved extraction consistency.

---

# Cost Analysis

Model Used:
- Gemini 2.5 Flash

| Metric | Value |
|---|---|
| Total Inputs Processed | 20 |
| Final Total Cost | ~$0.0085 |
| Average Cost Per Input | ~$0.00043 |
| Retry Overhead | Low |
| Reliability Improvement | Very High |

Although retries slightly increased token usage, the improvement in extraction reliability justified the additional cost.

---

# Key Observations

- Structured outputs alone were not fully reliable.
- Pydantic validation exposed hidden formatting problems.
- Gemini corrected most issues after receiving validation feedback.
- Self-repair loops dramatically improved robustness.
- Most recovery cases succeeded within 1 retry.

---

# Conclusion

Self-repair loops are essential for production-grade structured extraction systems.

Using:
- response_schema
- Pydantic validation
- validation-feedback retries

improved extraction success rate from:

40% → 100%

with minimal additional cost.

This approach is highly effective for:
- OCR pipelines
- business card extraction
- invoice processing
- onboarding systems
- document intelligence workflows