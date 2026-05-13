import csv
import time
from pathlib import Path
from google import genai

# ======================
# GEMINI CLIENT
# ======================

client = genai.Client(
    vertexai=True,
    project="wohlig",
    location="global"
)
# ======================
# MODELS
# ======================

MODELS = [
    "gemini-3.1-pro-preview",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite"
]

# ======================
# PRICING
# per 1M tokens
# ======================

PRICING = {
    "gemini-3.1-pro-preview": {
        "input": 2.00,
        "output": 12.00
    },
    "gemini-2.5-flash": {
        "input": 0.30,
        "output": 2.50
    },
    "gemini-2.5-flash-lite": {
        "input": 0.10,
        "output": 0.40
    }
}

# ======================
# INPUTS
# ======================

INPUT_DIR = Path("inputs")

# ======================
# OUTPUT CSV
# ======================

CSV_FILE = "results.csv"

# ======================
# PROMPT
# ======================

PROMPT = """
Summarize the following document into exactly 3 concise bullet points.

Document:
{document}
"""

# ======================
# CSV HEADERS
# ======================

headers = [
    "input_id",
    "model",
    "latency_ms",
    "input_tokens",
    "output_tokens",
    "cost_usd",
    "quality_score_1to5",
    "notes"
]

# ======================
# RUN
# ======================

with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)
    writer.writerow(headers)

    for input_file in INPUT_DIR.glob("*.txt"):

        document = input_file.read_text(
            encoding="utf-8"
        )

        print(f"\nProcessing: {input_file.name}")

        for model_name in MODELS:

            try:

                prompt = PROMPT.format(
                    document=document
                )

                # Start timer
                start = time.time()

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                # End timer
                end = time.time()

                latency_ms = round(
                    (end - start) * 1000,
                    2
                )

                output_text = response.text

                # Usage metadata
                usage = response.usage_metadata

                input_tokens = (
                    usage.prompt_token_count
                )

                output_tokens = (
                    usage.candidates_token_count
                )

                # Cost calculation
                input_cost = (
                    input_tokens / 1_000_000
                ) * PRICING[model_name]["input"]

                output_cost = (
                    output_tokens / 1_000_000
                ) * PRICING[model_name]["output"]

                cost_usd = round(
                    input_cost + output_cost,
                    8
                )

                judge_prompt = f"""
                You are evaluating a summary.

                Rate the summary from 1 to 5 based on:
                - accuracy
                - clarity
                - completeness

                Also provide a very short note.

                Return in this format only:

                Score: <number>
                Note: <short note>

                Original Document:
                {document}

                Summary:
                {output_text}
                """

                judge_response = client.models.generate_content(
                    model="gemini-2.5-pro",
                    contents=judge_prompt
                )

                judge_text = judge_response.text.strip()

                lines = judge_text.split("\n")

                quality_score_1to5 = lines[0].replace(
                    "Score:",
                    ""
                ).strip()

                note = lines[1].replace(
                    "Note:",
                    ""
                ).strip()

                writer.writerow([
                    input_file.stem,
                    model_name,
                    latency_ms,
                    input_tokens,
                    output_tokens,
                    cost_usd,
                    quality_score_1to5,
                    note
                ])

                print(
                    f"Done: {input_file.stem} | {model_name}"
                )

            except Exception as e:

                print(
                    f"Error with {model_name}: {e}"
                )

print("\nCompleted Successfully")