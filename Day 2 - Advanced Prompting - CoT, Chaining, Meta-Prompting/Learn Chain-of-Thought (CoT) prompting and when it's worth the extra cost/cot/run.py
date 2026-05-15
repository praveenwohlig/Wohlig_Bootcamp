import json
import pandas as pd
from collections import Counter
from dotenv import load_dotenv
from google import genai
import os

# =============================
# LOAD ENV
# =============================

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID", "")
LOCATION = os.getenv("LOCATION", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

# =============================
# GEMINI CLIENT
# =============================

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
)

# =============================
# TOKEN PRICING
# Change according to model pricing
# Example pricing only
# =============================

INPUT_PRICE_PER_1M = 0.35
OUTPUT_PRICE_PER_1M = 1.05

# =============================
# LOAD FILES
# =============================

print("Loading scenarios and prompts...")

with open("scenarios.jsonl") as f:
    scenarios = [json.loads(line) for line in f]

with open("prompts/direct.txt") as f:
    DIRECT_PROMPT = f.read()

with open("prompts/cot.txt") as f:
    COT_PROMPT = f.read()

print(f"Loaded {len(scenarios)} scenarios")

# =============================
# HELPER
# =============================

def calculate_cost(input_tokens, output_tokens):

    input_cost = (input_tokens / 1_000_000) * INPUT_PRICE_PER_1M
    output_cost = (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_1M

    total_cost = input_cost + output_cost

    return round(total_cost, 8)


def ask_model(prompt, temperature=0):

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": temperature
        }
    )

    text = response.text.strip()

    usage = response.usage_metadata

    input_tokens = usage.prompt_token_count
    output_tokens = usage.candidates_token_count

    cost = calculate_cost(
        input_tokens,
        output_tokens
    )

    return {
        "text": text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": cost
    }

# =============================
# RUN EXPERIMENT
# =============================

results = []

print("\nStarting experiment...\n")

for idx, item in enumerate(scenarios, start=1):

    scenario = item["scenario"]
    truth = item["ground_truth"]

    print("=" * 60)
    print(f"Scenario {idx}")
    print("=" * 60)

    print("\nScenario Text:")
    print(scenario)

    # =========================
    # DIRECT
    # =========================

    print("\nRunning DIRECT prompting...")

    direct_prompt = DIRECT_PROMPT.format(
        scenario=scenario
    )

    direct_result = ask_model(
        direct_prompt,
        temperature=0
    )

    direct_answer = direct_result["text"]

    print(f"Direct Answer: {direct_answer}")
    print(f"Direct Cost: ${direct_result['cost']}")

    # =========================
    # COT
    # =========================

    print("\nRunning CoT prompting...")

    cot_prompt = COT_PROMPT.format(
        scenario=scenario
    )

    cot_result = ask_model(
        cot_prompt,
        temperature=0
    )

    cot_answer = cot_result["text"]

    print(f"CoT Answer: {cot_answer}")
    print(f"CoT Cost: ${cot_result['cost']}")

    # =========================
    # SELF CONSISTENCY
    # =========================

    print("\nRunning Self-Consistency...")

    sc_answers = []
    sc_total_cost = 0

    for run in range(1, 6):

        print(f"SC Run {run}/5")

        sc_result = ask_model(
            cot_prompt,
            temperature=0.7
        )

        ans = sc_result["text"]

        sc_answers.append(ans)

        sc_total_cost += sc_result["cost"]

        print(f"Answer: {ans}")
        print(f"Run Cost: ${sc_result['cost']}")

    majority_answer = Counter(sc_answers).most_common(1)[0][0]

    print(f"\nMajority Answer: {majority_answer}")
    print(f"SC Total Cost: ${round(sc_total_cost, 8)}")

    # =========================
    # SAVE RESULTS
    # =========================

    results.append({

        "scenario_id": item["scenario_id"],

        "direct_answer": direct_answer,
        "direct_correct": direct_answer == truth,

        "cot_answer": cot_answer,
        "cot_correct": cot_answer == truth,

        "sc_answer": majority_answer,
        "sc_correct": majority_answer == truth,

        "direct_cost_usd": direct_result["cost"],
        "cot_cost_usd": cot_result["cost"],
        "sc_cost_usd": round(sc_total_cost, 8)

    })

    print("\nScenario Completed")

# =============================
# EXPORT CSV
# =============================

print("\nSaving results.csv ...")

df = pd.DataFrame(results)

df.to_csv("results.csv", index=False)

print("\nresults.csv saved successfully!")

# =============================
# ACCURACY SUMMARY
# =============================

print("\n" + "=" * 60)
print("FINAL ACCURACY")
print("=" * 60)

print(
    f"Direct Accuracy: "
    f"{df['direct_correct'].mean() * 100:.2f}%"
)

print(
    f"CoT Accuracy: "
    f"{df['cot_correct'].mean() * 100:.2f}%"
)

print(
    f"Self-Consistency Accuracy: "
    f"{df['sc_correct'].mean() * 100:.2f}%"
)

# =============================
# TOTAL COST
# =============================

print("\n" + "=" * 60)
print("TOTAL COST")
print("=" * 60)

print(
    f"Direct Total Cost: "
    f"${df['direct_cost_usd'].sum():.8f}"
)

print(
    f"CoT Total Cost: "
    f"${df['cot_cost_usd'].sum():.8f}"
)

print(
    f"SC Total Cost: "
    f"${df['sc_cost_usd'].sum():.8f}"
)

print("\nExperiment completed successfully!")