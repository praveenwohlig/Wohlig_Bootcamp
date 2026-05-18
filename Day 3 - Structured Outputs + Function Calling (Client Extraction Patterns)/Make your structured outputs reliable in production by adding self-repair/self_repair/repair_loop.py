import os
import json
import csv
import logging
from pathlib import Path
from dotenv import load_dotenv
from google.genai import types
from google import genai
from pydantic import ValidationError

from schema import ContactCard

load_dotenv()


PROJECT_ID = os.getenv("PROJECT_ID","")
LOCATION = os.getenv("LOCATION","")
MODEL_NAME = os.getenv("MODEL_NAME","")
logging.basicConfig(
    filename="repair.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class GeminiRepairExtractor:

    MAX_RETRIES = 3

    def __init__(self):
        self.client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=LOCATION,
        )

        self.model = MODEL_NAME

        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def generate_response(self, prompt: str):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=ContactCard
            )
        )

        usage = response.usage_metadata

        input_tokens = getattr(usage, "prompt_token_count", 0)
        output_tokens = getattr(usage, "candidates_token_count", 0)

        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

        return response.text

    def calculate_cost(self):

        input_cost = self.total_input_tokens * 0.0000003
        output_cost = self.total_output_tokens * 0.0000025

        return round(input_cost + output_cost, 6)

    def build_prompt(self, text: str):

        return f"""
You are a strict JSON extraction engine.

Extract contact information from noisy OCR text.

Rules:
- Return ONLY valid JSON
- Follow schema strictly
- Phone must contain exactly 10 digits
- Pincode must contain exactly 6 digits
- Do not hallucinate values
- If value unavailable return null

OCR INPUT:
{text}
"""

    def build_repair_prompt(
        self,
        original_input: str,
        previous_output: str,
        validation_error: str
    ):

        return f"""
The previous JSON response was invalid.

ORIGINAL OCR INPUT:
{original_input}

PREVIOUS INVALID OUTPUT:
{previous_output}

VALIDATION ERROR:
{validation_error}

Fix the response.

Return ONLY valid JSON.
"""

    def process_input(self, input_id: str, text: str):

        retries = 0
        errors_seen = []

        prompt = self.build_prompt(text)

        first_try_valid = False

        while retries <= self.MAX_RETRIES:

            try:

                response_text = self.generate_response(prompt)

                parsed = json.loads(response_text)

                validated = ContactCard.model_validate(parsed)

                if retries == 0:
                    first_try_valid = True

                return {
                    "input_id": input_id,
                    "first_try_valid": first_try_valid,
                    "final_valid": True,
                    "num_retries": retries,
                    "errors_seen": " | ".join(errors_seen),
                    "total_cost": self.calculate_cost()
                }

            except (
                json.JSONDecodeError,
                ValidationError,
                Exception
            ) as e:

                error_message = str(e)

                logging.error(error_message)

                errors_seen.append(error_message)

                retries += 1

                if retries > self.MAX_RETRIES:

                    return {
                        "input_id": input_id,
                        "first_try_valid": False,
                        "final_valid": False,
                        "num_retries": retries,
                        "errors_seen": " | ".join(errors_seen),
                        "total_cost": self.calculate_cost()
                    }

                prompt = self.build_repair_prompt(
                    original_input=text,
                    previous_output=response_text,
                    validation_error=error_message
                )


def main():

    extractor = GeminiRepairExtractor()

    input_dir = Path("inputs")

    results = []

    for file in sorted(input_dir.glob("*.txt")):

        input_id = file.stem

        text = file.read_text(encoding="utf-8")

        result = extractor.process_input(
            input_id=input_id,
            text=text
        )

        results.append(result)

        print(f"Processed: {input_id}")

    with open("results.csv", "w", newline="", encoding="utf-8") as csv_file:

        fieldnames = [
            "input_id",
            "first_try_valid",
            "final_valid",
            "num_retries",
            "errors_seen",
            "total_cost"
        ]

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    print("\nEvaluation Completed")
    print(f"Total Cost: ${extractor.calculate_cost()}")


if __name__ == "__main__":
    main()