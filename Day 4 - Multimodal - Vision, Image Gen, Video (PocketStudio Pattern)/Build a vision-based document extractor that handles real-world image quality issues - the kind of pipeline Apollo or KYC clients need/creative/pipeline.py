import os
import json
import uuid
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.cloud import storage

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION", "us-central1")
BUCKET_NAME = os.getenv("BUCKET_NAME","")

# =========================================================
# COST CONFIG (REALISTIC ESTIMATE)
# =========================================================

GEN_COST_PER_IMAGE = 0.039
BRAND_CHECK_COST = 0.0015

# =========================================================
# STYLE VARIATIONS
# =========================================================

STYLE_VARIATIONS = [
    "luxury festive cinematic lighting",
    "minimal premium studio aesthetic",
    "winter luxury commercial campaign"
]

# =========================================================
# CLIENTS
# =========================================================

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION
)

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# =========================================================
# HELPERS
# =========================================================

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def upload_to_gcs(local_path, gcs_path):

    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)

    print(f"Uploaded -> gs://{BUCKET_NAME}/{gcs_path}")

# =========================================================
# IMAGE GENERATION
# =========================================================

def generate_image(
    input_image_path,
    final_prompt,
    output_path
):

    with open(input_image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[
            final_prompt,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )
        ],
        config=types.GenerateContentConfig(
            temperature=0.8
        )
    )

    saved = False

    for part in response.candidates[0].content.parts:

        if hasattr(part, "inline_data") and part.inline_data:

            with open(output_path, "wb") as f:
                f.write(part.inline_data.data)

            saved = True
            break

    if not saved:
        raise Exception("No image generated")

# =========================================================
# BRAND VALIDATION
# =========================================================

def validate_brand(
    image_path,
    guidelines,
    brand_prompt
):

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    final_prompt = f"""
{brand_prompt}

BRAND GUIDELINES:
{guidelines}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            final_prompt,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )
        ]
    )

    text = response.text.strip()

    try:
        cleaned = text.replace("```json", "").replace("```", "")
        return json.loads(cleaned)

    except Exception:

        return {
            "pass": False,
            "score": 0,
            "violations": ["Invalid JSON response"],
            "reasoning": text
        }

# =========================================================
# PROCESS SINGLE PRODUCT
# =========================================================

def process_product(product_dir):

    print(f"\nProcessing -> {product_dir}")

    product_dir = Path(product_dir)

    input_image = product_dir / "input.png"
    brief_file = product_dir / "brief.json"

    with open(brief_file, "r") as f:
        brief = json.load(f)

    guidelines = read_file(
        "brand_guidelines.md"
    )

    nano_prompt_template = read_file(
        "prompts/nano_banana_prompt.txt"
    )

    brand_prompt = read_file(
        "prompts/brand_check_prompt.txt"
    )

    product_name = brief["product"]

    run_dir = product_dir

    # copy brief
    save_json(
        run_dir / "brief.json",
        brief
    )

    brand_results = []

    # =====================================================
    # GENERATE 3 VARIANTS
    # =====================================================

    for idx, style in enumerate(STYLE_VARIATIONS):

        print(f"Generating Variant {idx+1}")

        final_prompt = nano_prompt_template.format(
            product=brief["product"],
            desired_mood=f"{brief['desired_mood']} + {style}",
            desired_background=brief["desired_background"],
            season=brief["season"],
            target_audience=brief["target_audience"]
        )

        variant_path = run_dir / f"variant_{idx+1}.jpg"

        # save prompt used
        with open(
            run_dir / f"variant_{idx+1}_prompt.txt",
            "w"
        ) as f:
            f.write(final_prompt)

        # ================================================
        # IMAGE GENERATION
        # ================================================

        generate_image(
            str(input_image),
            final_prompt,
            str(variant_path)
        )

        # ================================================
        # BRAND VALIDATION
        # ================================================

        validation = validate_brand(
            str(variant_path),
            guidelines,
            brand_prompt
        )

        brand_results.append({
            "variant": f"variant_{idx+1}.jpg",
            "validation": validation
        })

        # ================================================
        # UPLOAD TO GCS
        # ================================================

        upload_to_gcs(
            str(variant_path),
            f"{product_name}/variant_{idx+1}.jpg"
        )

    # =====================================================
    # SAVE BRAND CHECK
    # =====================================================

    brand_check_path = run_dir / "brand_check.json"

    save_json(
        brand_check_path,
        brand_results
    )

    upload_to_gcs(
        str(brand_check_path),
        f"{product_name}/brand_check.json"
    )

    # =====================================================
    # COST CALCULATION
    # =====================================================

    generation_cost = 3 * GEN_COST_PER_IMAGE
    validation_cost = 3 * BRAND_CHECK_COST
    total_cost = generation_cost + validation_cost

    return {
        "run_id": str(uuid.uuid4())[:8],
        "product": brief["product"],
        "variants_generated": 3,
        "gen_cost_usd": round(generation_cost, 4),
        "brand_check_cost_usd": round(validation_cost, 4),
        "total_cost_usd": round(total_cost, 4)
    }

# =========================================================
# MAIN
# =========================================================

def main():

    products_root = Path("runs")

    all_costs = []

    for product_folder in products_root.iterdir():

        if product_folder.is_dir():

            try:

                result = process_product("runs/sku_004")

                all_costs.append(result)

                print(f"Completed -> {product_folder.name}")

            except Exception as e:

                print(f"Failed -> {product_folder.name}")
                print(str(e))

    # =====================================================
    # SAVE COST LOG
    # =====================================================

    # =====================================================
    # SAVE COST LOG
    # =====================================================

    cost_df = pd.DataFrame(all_costs)

    EXPECTED_COLUMNS = [
        "run_id",
        "product",
        "variants_generated",
        "gen_cost_usd",
        "brand_check_cost_usd",
        "total_cost_usd"
    ]

    cost_df = cost_df[EXPECTED_COLUMNS]

    cost_df.to_csv(
        "cost_log.csv",
        index=False
    )

    print("\nCost log updated successfully")

    print("\n===================================")
    print("Creative Pipeline Completed")
    print("===================================")

if __name__ == "__main__":
    main()