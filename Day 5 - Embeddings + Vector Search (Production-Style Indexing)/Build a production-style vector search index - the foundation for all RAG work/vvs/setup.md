# Vertex AI Vector Search - Setup Guide

---

# Project Overview

This project implements a production-style semantic retrieval pipeline using:

- Gemini Embedding API
- Vertex AI Vector Search
- PDF ingestion + chunking
- ANN (Approximate Nearest Neighbor) search
- Metadata filtering
- Retrieval-Augmented Generation (RAG) foundation

---

# Architecture

PDF Documents
↓
Text Extraction
↓
Chunking
↓
Gemini Embeddings
↓
Vertex AI Vector Search
↓
Semantic Retrieval
↓
Chunk Text Lookup

---

# Folder Structure

/vvs
├── corpus/
├── embeddings/
│   ├── vectors.json
│   └── chunk_store.json
├── ingest.py
├── query.py
├── corpus_manifest.csv
├── filtered_queries.md
└── setup.md

---

# Technologies Used

| Component | Technology |
|---|---|
| Embedding Model | Gemini text-embedding-005 |
| Vector Database | Vertex AI Vector Search |
| Cloud Storage | Google Cloud Storage |
| PDF Parsing | pypdf |
| Language | Python |
| ANN Algorithm | Tree-AH |

---

# Environment Variables

Create `.env`

```env
PROJECT_ID=your-project-id

LOCATION=us-central1

BUCKET_NAME=your-gcs-bucket

INDEX_ID=your-index-id

INDEX_ENDPOINT_ID=your-endpoint-id

DEPLOYED_INDEX_ID=your-deployed-index-id
```

---

# Install Dependencies

```bash
pip install google-genai
pip install google-cloud-aiplatform
pip install google-cloud-storage
pip install python-dotenv
pip install pandas
pip install tqdm
pip install pypdf
```

---

# Create GCS Bucket

Example:

```bash
gsutil mb gs://your-bucket-name
```

---

# Create Vertex AI Index

Recommended Configuration:

| Setting | Value |
|---|---|
| Algorithm | Tree-AH |
| Dimensions | 768 |
| Distance Metric | Dot Product |
| Approx Neighbors | 150 |
| Update Method | Streaming |
| Shard Size | Small |

---

# Create Endpoint

Create:
- Vertex AI Index Endpoint

Then:
- Deploy Index to Endpoint

---

# Embedding Details

Model Used:

text-embedding-005

Embedding Dimensions:

768

---

# Chunking Strategy

Chunk Size:

512 words

Chunking Method:
- Simple word-based chunking

---

# Metadata Restricts

Current Metadata:

```json
{
  "doc_type": "report",
  "page_number": 5
}
```

Supported Filtering:

```python
doc_type_filter="report"
```

---

# Ingestion Pipeline

Run:

```bash
python ingest.py
```

Pipeline Steps:

1. Parse PDFs
2. Extract Text
3. Chunk Text
4. Generate Embeddings
5. Save chunk_store.json
6. Create vectors.json
7. Upload vectors to GCS
8. Upsert vectors into Vertex AI Index

---

# Query Pipeline

Run:

```bash
python query.py
```

Pipeline Steps:

1. Generate query embedding
2. Perform semantic search
3. Retrieve nearest vectors
4. Lookup original chunk text
5. Display retrieved chunks

---

# Example Query

```python
results = search(
    question="committee meetings",
    top_k=5,
    doc_type_filter="report"
)
```

---

# Example Output

```txt
Result 1

Similarity Score: 0.684

Metadata:
{
  "doc_id": "rbi_general_regulations",
  "page_number": 5
}

Retrieved Text:
"MEETINGS OF CENTRAL AND LOCAL BOARDS..."
```

---

# ANN Search

This project uses:

Tree-AH (Approximate Nearest Neighbor)

Benefits:
- Fast retrieval
- Scalable semantic search
- Optimized vector similarity lookup

---

# Production Architecture

| Component | Purpose |
|---|---|
| Vertex AI Vector Search | Semantic retrieval |
| chunk_store.json | Original text storage |
| Gemini Embeddings | Semantic encoding |
| query.py | Retrieval orchestration |
| ingest.py | Data ingestion |

---

# Future Improvements

Possible enhancements:

- Hybrid search
- BM25 + Vector Search
- Multi-document filtering
- Re-ranking
- Gemini answer generation
- LangChain integration
- Streaming ingestion
- OCR support
- Semantic caching

---

# Learning Outcomes

This project demonstrates:

- Semantic search
- Vector embeddings
- ANN indexing
- Metadata filtering
- Cloud vector databases
- RAG architecture
- Production AI infrastructure
- Vertex AI Vector Search
