# =========================================================
# ingest.py
# Production-Style Vertex AI Vector Search Ingestion
# =========================================================

import os
import json
import uuid
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
from pypdf import PdfReader

from google import genai
from google.cloud import storage
from google.cloud import aiplatform
from google.cloud.aiplatform_v1.types import IndexDatapoint

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")

LOCATION = os.getenv(
    "LOCATION",
    "us-central1"
)

BUCKET_NAME = os.getenv(
    "BUCKET_NAME", ""
)

INDEX_ID = os.getenv(
    "INDEX_ID", ""
)

# =========================================================
# CONFIG
# =========================================================

CORPUS_DIR = "corpus"

EMBED_MODEL = "text-embedding-005"

CHUNK_SIZE = 512

UPSERT_BATCH_SIZE = 100

# =========================================================
# CLIENTS
# =========================================================

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION
)

storage_client = storage.Client()

bucket = storage_client.bucket(
    BUCKET_NAME
)

aiplatform.init(
    project=PROJECT_ID,
    location=LOCATION
)

# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    pages = []

    for page_num, page in enumerate(
        reader.pages
    ):

        text = page.extract_text()

        pages.append({
            "page_number": page_num + 1,
            "text": text if text else ""
        })

    return pages

# =========================================================
# CHUNKING
# =========================================================

def chunk_text(
    text,
    chunk_size=512
):

    words = text.split()

    chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunks.append(chunk)

    return chunks

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
# GCS UPLOAD
# =========================================================

def upload_to_gcs(
    local_path,
    gcs_path
):

    blob = bucket.blob(gcs_path)

    blob.upload_from_filename(
        local_path
    )

    print(
        f"Uploaded -> gs://{BUCKET_NAME}/{gcs_path}"
    )

# =========================================================
# VECTOR RECORD
# =========================================================

def create_vector_record(
        chunk,
    embedding,
    metadata
):

    return {
        "id": str(uuid.uuid4()),
        "text": chunk,
        "embedding": embedding,
        "metadata": metadata
    }

# =========================================================
# BUILD INDEX DATAPOINTS
# =========================================================

def build_index_datapoints(vector_records):

    datapoints = []

    for record in vector_records:

        restriction = IndexDatapoint.Restriction(
            namespace="doc_type",
            allow_list=[
                record["metadata"]["doc_type"]
            ]
        )

        dp = IndexDatapoint(
            datapoint_id=record["id"],
            feature_vector=record["embedding"],
            restricts=[restriction]
        )

        datapoints.append(dp)

    return datapoints

# =========================================================
# UPSERT INTO VERTEX AI INDEX
# =========================================================

def upsert_to_index(vector_records):

    print(
        f"\nUpserting {len(vector_records)} vectors into Vertex AI Index..."
    )

    index = aiplatform.MatchingEngineIndex(
        index_name=INDEX_ID
    )

    datapoints = build_index_datapoints(
        vector_records
    )

    total_batches = (
        len(datapoints) + UPSERT_BATCH_SIZE - 1
    ) // UPSERT_BATCH_SIZE

    for i in range(
        0,
        len(datapoints),
        UPSERT_BATCH_SIZE
    ):

        batch = datapoints[
            i:i + UPSERT_BATCH_SIZE
        ]

        batch_num = (i // UPSERT_BATCH_SIZE) + 1

        index.upsert_datapoints(
            datapoints=batch
        )

        print(
            f"  Upserted batch {batch_num}/{total_batches} "
            f"({len(batch)} vectors)"
        )

    print(
        f"\nAll {len(datapoints)} vectors upserted successfully."
    )

# =========================================================
# MAIN INGESTION
# =========================================================

def ingest_corpus():

    corpus_path = Path(CORPUS_DIR)

    manifest_rows = []

    vector_records = []

    # =====================================================
    # PROCESS PDFs
    # =====================================================

    for pdf_file in tqdm(
        list(corpus_path.glob("*.pdf"))
    ):

        print(f"\nProcessing: {pdf_file.name}")

        doc_id = pdf_file.stem

        # =================================================
        # METADATA
        # =================================================

        doc_type = "report"

        pages = extract_text_from_pdf(
            pdf_file
        )

        total_chunks = 0

        # =================================================
        # PAGE LOOP
        # =================================================

        for page in pages:

            page_number = page["page_number"]

            page_text = page["text"]

            chunks = chunk_text(
                page_text,
                chunk_size=CHUNK_SIZE
            )

            for chunk in chunks:

                if len(chunk.strip()) == 0:
                    continue

                # =========================================
                # GENERATE EMBEDDING
                # =========================================

                embedding = generate_embedding(
                    chunk
                )

                # =========================================
                # METADATA
                # =========================================

                metadata = {
                    "doc_id": doc_id,
                    "doc_type": doc_type,
                    "page_number": page_number
                }

                # =========================================
                # VECTOR RECORD
                # =========================================

                vector_record = (
                    create_vector_record(
                        chunk,
                        embedding,
                        metadata
                    )
                )

                vector_records.append(
                    vector_record
                )

                total_chunks += 1

        # =================================================
        # MANIFEST ENTRY
        # =================================================

        manifest_rows.append({
            "doc_id": doc_id,
            "title": pdf_file.name,
            "doc_type": doc_type,
            "num_pages": len(pages),
            "num_chunks": total_chunks
        })

    # =====================================================
    # CREATE JSON
    # =====================================================

    os.makedirs(
        "embeddings",
        exist_ok=True
    )

    vectors_path = "embeddings/vectors.json"
    # =====================================================
    # SAVE CHUNK STORE
    # =====================================================

    with open(
            "embeddings/chunk_store.json",
            "w"
    ) as f:

        json.dump(
            vector_records,
            f,
            indent=2
        )

    print(
        "\nSaved embeddings/chunk_store.json"
    )


    with open(vectors_path, "w") as f:

        for record in vector_records:

            vertex_record = {

                "id": record["id"],

                "embedding": (
                    record["embedding"]
                ),

                "restricts": [
                    {
                        "namespace": "doc_type",
                        "allow": [
                            record["metadata"]["doc_type"]
                        ]
                    }
                ]
            }

            f.write(
                json.dumps(vertex_record) + "\n"
            )

    print("\nSaved embeddings/vectors.json")

    # =====================================================
    # UPLOAD TO GCS
    # =====================================================

    upload_to_gcs(
        vectors_path,
        "vectors/vectors.json"
    )

    # =====================================================
    # UPSERT INTO VERTEX AI INDEX  <-- NEW
    # =====================================================

    upsert_to_index(vector_records)

    # =====================================================
    # SAVE MANIFEST CSV
    # =====================================================

    manifest_df = pd.DataFrame(manifest_rows)

    manifest_df.to_csv(
        "corpus_manifest.csv",
        index=False
    )

    print("\nSaved corpus_manifest.csv")

    # =====================================================
    # DONE
    # =====================================================

    print("\n===================================")

    print("Ingestion complete!")

    print(
        f"\nVectors uploaded to:\n"
        f"gs://{BUCKET_NAME}/vectors/vectors.json"
    )

    print(
        f"\nVectors upserted into Vertex AI Index:\n"
        f"{INDEX_ID}"
    )

    print("===================================")

# =========================================================
# ENTRY
# =========================================================

if __name__ == "__main__":

    ingest_corpus()