import json
import os
import sys

from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from schema import InvoiceExtraction

# ====================================
# LOAD ENV
# ====================================

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID","")
LOCATION = os.getenv("LOCATION","")
MODEL_NAME = os.getenv("MODEL_NAME","")

if not PROJECT_ID or not LOCATION or not MODEL_NAME:
    raise ValueError(
        "Missing PROJECT_ID / LOCATION / MODEL_NAME in .env"
    )

# ====================================
# GENAI CLIENT
# ====================================

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
)

# ====================================
# VALIDATE FILE
# ====================================

def validate_file(file_path):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    allowed_extensions = [
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg"
    ]

    if path.suffix.lower() not in allowed_extensions:
        raise ValueError(
            f"Unsupported file type: {path.suffix}"
        )

# ====================================
# EXTRACT INVOICE
# ====================================

def extract_invoice(file_path):

    validate_file(file_path)

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    prompt = """
You are an enterprise invoice extraction AI.

Extract structured invoice data from this document.

IMPORTANT RULES:
- Return valid structured JSON only
- Follow the response schema strictly
- Do not hallucinate values
- Use null for missing fields
- Extract all visible line items
- Preserve numeric accuracy
- Normalize dates into YYYY-MM-DD format
- Extract status carefully:
  PAID / UNPAID / OVERDUE
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Part.from_bytes(
                data=file_bytes,
                mime_type="application/pdf"
            ),
            prompt
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=InvoiceExtraction,
            temperature=0
        )
    )

    return response.parsed
# ====================================
# MAIN
# ====================================

def main():

    if len(sys.argv) < 2:

        print(
            "Usage: python main.py <file_path>"
        )

        sys.exit(1)

    file_path = sys.argv[1]

    try:

        result = extract_invoice(file_path)

        print(
            json.dumps(
                result.model_dump(),
                indent=2
            )
        )

    except Exception as e:

        print(f"\nERROR: {e}")

# ====================================
# ENTRY
# ====================================

if __name__ == "__main__":
    main()