import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load env
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID", "")
LOCATION = os.getenv("LOCATION", "us-central1")
MODEL_NAME = os.getenv("MODEL_NAME", "veo-3.1-generate-001")

# Create Vertex AI client
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION
)

PROMPT = """
A futuristic black sneaker floating above a glossy reflective platform in a neon-lit studio.
Slow dolly-in camera movement.
Golden hour rim lighting with cinematic shadows.
Shallow depth of field.
Smooth rotating product showcase.
Premium sports commercial aesthetic.
"""

OUTPUT_DIR = "iterations/v2"
OUTPUT_FILE = f"{OUTPUT_DIR}/output.mp4"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read local image
with open("reference.png", "rb") as img:
    image_bytes = img.read()

print("Reference image loaded")

# Generate Veo video
operation = client.models.generate_videos(
    model=MODEL_NAME,
    prompt=PROMPT,
    image=types.Image(
        image_bytes=image_bytes,
        mime_type="image/png"
    ),
    config=types.GenerateVideosConfig(
        duration_seconds=8
    )
)

print("Generating video...")

# Poll operation
while not operation.done:
    time.sleep(10)
    print("Waiting for generation...")
    operation = client.operations.get(operation)

# Check errors
if operation.error:
    print("Generation failed:")
    print(operation.error)
    exit()

# Get response
video_response = operation.response

generated_video = video_response.generated_videos[0]

# Save video
generated_video.video.save(OUTPUT_FILE)

print(f"Video saved at: {OUTPUT_FILE}")