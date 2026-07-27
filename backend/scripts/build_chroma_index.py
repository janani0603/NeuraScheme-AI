"""
build_chroma_index.py
─────────────────────
One-time script: reads all schemes from MongoDB → builds ChromaDB vector index.

Run from backend\ directory:
    venv\Scripts\python.exe scripts\build_chroma_index.py

Safe to re-run — clears and rebuilds the collection each time.
"""

import os
import sys
import ast
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

import chromadb
from chromadb.config import Settings as ChromaSettings
from pymongo import MongoClient
from tqdm import tqdm

from app.agents.embedding_model import embed_batch

# ── Config ────────────────────────────────────────────────────────────────────
MONGODB_URI   = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "neurascheme")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(BASE_DIR / "chroma_db"))
COLLECTION_NAME = "schemes"
BATCH_SIZE = 100

print("\n===================================")
print(" NeuraScheme AI — Build Chroma Index")
print("===================================\n")

# ── MongoDB ───────────────────────────────────────────────────────────────────
print("Connecting to MongoDB...")
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client[DATABASE_NAME]
schemes = list(db["schemes"].find({}, {
    "slug": 1, "scheme_name": 1, "search_text": 1,
    "level": 1, "schemeCategory": 1, "tags": 1,
    "eligibility": 1, "benefits": 1, "details": 1,
}))
mongo_client.close()
print(f"Loaded {len(schemes)} schemes from MongoDB\n")

if not schemes:
    print("No schemes found. Run import_dataset.py first.")
    sys.exit(1)

# ── ChromaDB ──────────────────────────────────────────────────────────────────
print(f"ChromaDB path: {CHROMA_DB_PATH}")
chroma_client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH,
    settings=ChromaSettings(anonymized_telemetry=False),
)

# Clear existing collection and recreate
try:
    chroma_client.delete_collection(COLLECTION_NAME)
    print("Cleared existing collection")
except Exception:
    pass

collection = chroma_client.create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)
print("Created fresh collection\n")

# ── Build index in batches ────────────────────────────────────────────────────
print("Generating embeddings and indexing...\n")

def _safe_str(val) -> str:
    if val is None:
        return ""
    if isinstance(val, list):
        return ", ".join(str(v) for v in val)
    return str(val)

def _safe_list_str(val) -> str:
    """Convert list or string-encoded list to comma-separated string for metadata."""
    if val is None:
        return ""
    if isinstance(val, list):
        return ", ".join(str(v) for v in val)
    try:
        parsed = ast.literal_eval(str(val))
        if isinstance(parsed, list):
            return ", ".join(str(v) for v in parsed)
    except Exception:
        pass
    return str(val)

total_indexed = 0

for i in tqdm(range(0, len(schemes), BATCH_SIZE), desc="Indexing batches"):
    batch = schemes[i:i + BATCH_SIZE]

    ids = []
    texts = []
    metadatas = []

    for scheme in batch:
        slug = scheme.get("slug", "")
        if not slug:
            continue

        # Build rich search text: search_text + eligibility + benefits
        search_text = _safe_str(scheme.get("search_text", ""))
        eligibility  = _safe_str(scheme.get("eligibility", ""))
        benefits     = _safe_str(scheme.get("benefits", ""))
        combined = f"{search_text} {eligibility} {benefits}".strip()

        ids.append(slug)
        texts.append(combined if combined else scheme.get("scheme_name", slug))

        # Metadata — ChromaDB only supports str/int/float/bool values
        metadatas.append({
            "scheme_name": _safe_str(scheme.get("scheme_name")),
            "level":       _safe_str(scheme.get("level")),
            "categories":  _safe_list_str(scheme.get("schemeCategory")),
            "tags":        _safe_list_str(scheme.get("tags")),
        })

    if not ids:
        continue

    # Generate embeddings for the batch
    embeddings = embed_batch(texts)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )
    total_indexed += len(ids)

# ── Summary ───────────────────────────────────────────────────────────────────
print(f"\n===================================")
print(f" Chroma Index Built Successfully")
print(f"===================================")
print(f" Collection : {COLLECTION_NAME}")
print(f" Documents  : {total_indexed}")
print(f" Path       : {CHROMA_DB_PATH}")
print(f"===================================\n")
