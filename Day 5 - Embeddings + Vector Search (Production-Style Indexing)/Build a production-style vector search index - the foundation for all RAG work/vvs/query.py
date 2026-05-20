# =========================================================
# query.py
# Production Vertex AI Vector Search Query
# =========================================================

import os
import json

from dotenv import load_dotenv

from google import genai
from google.cloud import aiplatform

from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")

LOCATION = os.getenv(
    "LOCATION",
    "us-central1"
)

INDEX_ENDPOINT_ID = os.getenv(
    "INDEX_ENDPOINT_ID",
    ""
)

DEPLOYED_INDEX_ID = os.getenv(
    "DEPLOYED_INDEX_ID",
    ""
)

EMBED_MODEL = "text-embedding-005"

# =========================================================
# CLIENTS
# =========================================================

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION
)

aiplatform.init(
    project=PROJECT_ID,
    location=LOCATION
)

# =========================================================
# LOAD CHUNK STORE
# =========================================================

with open(
    "embeddings/chunk_store.json",
    "r"
) as f:

    CHUNK_STORE = json.load(f)

# =========================================================
# CHUNK LOOKUP
# =========================================================

chunk_lookup = {
    item["id"]: item
    for item in CHUNK_STORE
}

# =========================================================
# EMBEDDING
# =========================================================

def generate_embedding(text):

    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=text
    )

    return response.embeddings[0].values

# =========================================================
# SEARCH
# =========================================================

def search(
    question,
    top_k=5,
    doc_type_filter=None
):

    print(f"\nQuery: {question}")

    # =====================================================
    # QUERY EMBEDDING
    # =====================================================

    query_embedding = generate_embedding(
        question
    )

    # =====================================================
    # INDEX ENDPOINT
    # =====================================================

    endpoint = (
        aiplatform.MatchingEngineIndexEndpoint(
            index_endpoint_name=
            INDEX_ENDPOINT_ID
        )
    )

    # =====================================================
    # FILTERS
    # =====================================================

    filter_list = []

    if doc_type_filter:

        filter_list.append(
            Namespace(
                name="doc_type",
                allow_tokens=[
                    doc_type_filter
                ]
            )
        )

    # =====================================================
    # VECTOR SEARCH
    # =====================================================

    response = endpoint.find_neighbors(

        deployed_index_id=
        DEPLOYED_INDEX_ID,

        queries=[query_embedding],

        num_neighbors=top_k,

        filter=filter_list
    )

    return response

# =========================================================
# EXAMPLE QUERY
# =========================================================

if __name__ == "__main__":

    results = search(

        question=
        "FORM OF DECLARATION OF FIDELITY AND SECRECY",

        top_k=5,

        doc_type_filter="report"
    )

    print("\n===================================")

    neighbors = results[0]

    for idx, neighbor in enumerate(neighbors):

        print(f"\nResult {idx+1}")

        print(
            f"\nSimilarity Score: "
            f"{neighbor.distance}"
        )

        chunk_data = chunk_lookup.get(
            neighbor.id
        )

        if chunk_data:

            print(
                f"\nMetadata:\n"
                f"{chunk_data['metadata']}"
            )

            print(
                f"\nRetrieved Text:\n"
                f"{chunk_data['text'][:1000]}"
            )

        print(
            "\n-----------------------------------"
        )

    print("\n===================================")