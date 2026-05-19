import os
import json
import csv
import time
import uuid
from pathlib import Path
from dotenv import load_dotenv

from google import genai
from google.genai import types

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID", "")
LOCATION = os.getenv("LOCATION", "us-central1")

# =========================================================
# CLIENT
# =========================================================

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION
)

# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

PRODUCTS_DIR = BASE_DIR / "products"
RUNS_DIR = BASE_DIR / "runs"
PROMPTS_DIR = BASE_DIR / "prompts"

RUNS_DIR.mkdir(exist_ok=True)

BRAND_GUIDELINES_PATH = BASE_DIR / "brand_guidelines.md"

# =========================================================
# LOAD BRAND GUIDELINES
# =========================================================

with open(BRAND_GUIDELINES_PATH, "r") as file:
    BRAND_GUIDELINES = file.read()

# =========================================================
# STYLE VARIATIONS
# =========================================================

STYLE_VARIATIONS = [
    "luxury studio lighting with warm golden tones",
    "festive premium commercial aesthetic with glowing lights",
    "futuristic neon cyberpunk advertisement style"
]

# =========================================================
# COST SETTINGS (FAKE ESTIMATES)
# =========================================================

IMAGE_GEN_COST = 0.04
BRAND_CHECK_COST = 0.002

# =========================================================
# HELPERS
# =========================================================

def load_brief(brief_path):
    with open(brief_path, "r") as file:
        return json.load(file)


def generate_prompt(product, mood, background, variation):
    return f"""
    Product advertisement photography for {product}.

    Mood:
    {mood}

    Background:
    {background}

    Style Variation:
    {variation}

    Cinematic lighting.
    Premium commercial aesthetic.
    Product centered and clearly visible.
    High detail.
    Clean composition.
    """


def generate_variant(image_path, prompt, output_path):

    with open(image_path, "rb") as img:
        image_bytes = img.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[
            types.Part.from_text(text=prompt),
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )
        ],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"]
        )
    )

    image_data = None

    for part in response.candidates[0].content.parts:
        if part.inline_data:
            image_data = part.inline_data.data

    if image_data is None:
        raise Exception("No image generated")

    with open(output_path, "wb") as f:
        f.write(image_data)

def brand_check(image_path):

    with open(image_path, "rb") as img:
        image_bytes = img.read()

    prompt = f"""
    You are a brand compliance checker.

    Analyze the image against these brand guidelines:

    {BRAND_GUIDELINES}

    Return JSON format:
    {{
        "status": "PASS or FAIL",
        "reasoning": "short explanation",
        "violations": []
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_text(text=prompt),
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )
        ]
    )

    return response.text


def save_cost_log(run_id, variants):

    gen_cost = variants * IMAGE_GEN_COST
    brand_cost = variants * BRAND_CHECK_COST
    total = gen_cost + brand_cost

    csv_path = BASE_DIR / "cost_log.csv"

    file_exists = csv_path.exists()

    with open(csv_path, "a", newline="") as csvfile:

        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow([
                "run_id",
                "variants_generated",
                "gen_cost_usd",
                "brand_check_cost_usd",
                "total_cost_usd"
            ])

        writer.writerow([
            run_id,
            variants,
            gen_cost,
            brand_cost,
            total
        ])


# =========================================================
# MAIN PIPELINE
# =========================================================

def run_pipeline():

    TARGET_SKU = "sku_005"

    product_folders = [
        folder for folder in PRODUCTS_DIR.iterdir()
        if folder.is_dir() and folder.name == TARGET_SKU
    ]

    for product_folder in product_folders:

        print(f"\nProcessing: {product_folder.name}")

        image_path = product_folder / "input.png"
        brief_path = product_folder / "brief.json"

        brief = load_brief(brief_path)

        run_folder = RUNS_DIR / product_folder.name
        run_folder.mkdir(exist_ok=True)

        brand_results = {}

        for i, variation in enumerate(STYLE_VARIATIONS, start=1):

            print(f"Generating variant {i}")
            time.sleep(30)
            prompt = generate_prompt(
                brief["product"],
                brief["desired_mood"],
                brief["desired_background"],
                variation
            )

            variant_output = run_folder / f"variant_{i}.jpg"

            generate_variant(
                image_path=image_path,
                prompt=prompt,
                output_path=variant_output
            )

            print(f"Running brand check for variant {i}")

            check_result = brand_check(variant_output)

            brand_results[f"variant_{i}"] = check_result

        # Save brand checks
        brand_check_path = run_folder / "brand_check.json"

        with open(brand_check_path, "w") as file:
            json.dump(brand_results, file, indent=2)

        # Save cost
        run_id = str(uuid.uuid4())

        save_cost_log(
            run_id=run_id,
            variants=3
        )

        print(f"Completed: {product_folder.name}")


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    run_pipeline()