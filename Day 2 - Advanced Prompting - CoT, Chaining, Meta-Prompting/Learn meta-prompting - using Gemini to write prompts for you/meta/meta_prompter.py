import argparse
import csv
import json
import os

from pathlib import Path
from dotenv import load_dotenv
from google import genai

# ====================================
# LOAD ENV VARIABLES
# ====================================

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID", "")
LOCATION = os.getenv("LOCATION", "")
MODEL_NAME = os.getenv("MODEL_NAME", "")

if not PROJECT_ID or not LOCATION or not MODEL_NAME:
    raise ValueError("Missing PROJECT_ID / LOCATION / MODEL_NAME in .env")

# ====================================
# GENAI CLIENT (VERTEX AI)
# ====================================

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
)


# ====================================
# LOAD META PROMPT
# ====================================

def load_meta_prompt():

    path = Path("meta_prompt.txt")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ====================================
# GENERATE PROMPT
# ====================================

def generate_prompt(user_brief):

    meta_prompt = load_meta_prompt()

    final_prompt = meta_prompt.replace(
        "{{USER_BRIEF}}",
        user_brief
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=final_prompt
    )

    return response.text


# ====================================
# GEMINI AS JUDGE
# ====================================

def judge_prompt_quality(prompt_text):

    judge_prompt = f"""
You are a senior Prompt Engineering evaluator.

Evaluate the following generated prompt.

CHECK THESE THINGS:
1. Does it contain all 6 required sections?
   - Role
   - Context
   - Task
   - Constraints
   - Format
   - Examples

2. Rate overall quality from 1–5 based on:
   - clarity
   - structure
   - constraints
   - examples
   - production readiness
   - formatting

3. Identify what is missing or weak.

IMPORTANT:
Return ONLY valid JSON.

Expected JSON format:

{{
  "quality_score": 5,
  "has_all_6_sections": true,
  "what_was_missing": "None"
}}

PROMPT TO EVALUATE:
--------------------

{prompt_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=judge_prompt
    )

    return response.text

# ====================================
# MAIN
# ====================================

def main():

    parser = argparse.ArgumentParser(
        description="Vertex AI Meta Prompter"
    )

    parser.add_argument(
        "brief",
        type=str,
        help="Vague project brief"
    )

    parser.add_argument(
        "--id",
        type=str,
        default="brief_1",
        help="Brief ID for saving files"
    )

    args = parser.parse_args()

    # ====================================
    # GENERATE PROMPT
    # ====================================

    generated_prompt = generate_prompt(args.brief)

    print("\n===== GENERATED PROMPT =====\n")
    print(generated_prompt)

    # ====================================
    # SAVE GENERATED PROMPT
    # ====================================

    # ====================================
    # JUDGE PROMPT QUALITY
    # ====================================

    judge_response = judge_prompt_quality(
        generated_prompt
    )

    print("\n===== JUDGE RESULT =====\n")
    print(judge_response)

    # ====================================
    # PARSE JUDGE RESPONSE
    # ====================================

    try:

        judge_json = json.loads(judge_response)

        quality_score = judge_json.get(
            "quality_score",
            0
        )

        has_all_sections = judge_json.get(
            "has_all_6_sections",
            False
        )

        what_was_missing = judge_json.get(
            "what_was_missing",
            "None"
        )

    except Exception:

        quality_score = 0

        has_all_sections = False

        what_was_missing = (
            "Failed to parse judge response"
        )

    print("\n===== SCORECARD SAVED =====")

# ====================================
# ENTRY POINT
# ====================================

if __name__ == "__main__":
    main()