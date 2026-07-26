"""
Generate and store embeddings for all schemes in MongoDB.

Usage:
    python scripts/generate_embeddings.py

Features:
- Skips schemes that already have embeddings
- Batch processing with progress bar
- Safe to interrupt and resume
"""
from pathlib import Path
import os
import sys

# Add backend root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import asyncio
from tqdm import tqdm
from pymongo import MongoClient, UpdateOne
from sentence_transformers import SentenceTransformer

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
BATCH_SIZE = 64


def build_embed_text(doc: dict) -> str:
    return " ".join(filter(None, [
        doc.get("scheme_name", ""),
        doc.get("details", ""),
        doc.get("benefits", ""),
        doc.get("eligibility", ""),
        " ".join(doc.get("schemeCategory", [])),
        " ".join(doc.get("tags", [])),
    ])).lower()


def main():
    print("\n===================================")
    print(" NeuraScheme AI Embedding Generator")
    print("===================================\n")

    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db["schemes"]

    # Count schemes without embeddings
    total_pending = collection.count_documents(
        {"$or": [{"embedding": None}, {"embedding": {"$exists": False}}]}
    )
    total_all = collection.count_documents({})

    print(f"Total schemes     : {total_all}")
    print(f"Already embedded  : {total_all - total_pending}")
    print(f"Pending           : {total_pending}")

    if total_pending == 0:
        print("\nAll schemes already have embeddings. Nothing to do.")
        client.close()
        return

    print(f"\nLoading model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("Model loaded.\n")

    # Fetch pending documents in batches
    cursor = collection.find(
        {"$or": [{"embedding": None}, {"embedding": {"$exists": False}}]},
        {"_id": 1, "scheme_name": 1, "details": 1, "benefits": 1,
         "eligibility": 1, "schemeCategory": 1, "tags": 1}
    )

    docs = list(cursor)
    processed = 0

    with tqdm(total=len(docs), desc="Generating embeddings") as pbar:
        for i in range(0, len(docs), BATCH_SIZE):
            batch = docs[i:i + BATCH_SIZE]
            texts = [build_embed_text(doc) for doc in batch]

            try:
                vectors = model.encode(
                    texts,
                    normalize_embeddings=True,
                    batch_size=BATCH_SIZE,
                    show_progress_bar=False,
                )
            except Exception as e:
                print(f"\nEmbedding error at batch {i}: {e}")
                continue

            operations = [
                UpdateOne(
                    {"_id": doc["_id"]},
                    {"$set": {"embedding": vector.tolist()}}
                )
                for doc, vector in zip(batch, vectors)
            ]

            try:
                collection.bulk_write(operations, ordered=False)
                processed += len(batch)
            except Exception as e:
                print(f"\nMongoDB write error at batch {i}: {e}")

            pbar.update(len(batch))

    print(f"\nEmbeddings generated : {processed}")
    print(f"Failed               : {len(docs) - processed}")
    print("\n===================================")
    print(" Embedding Generation Complete")
    print("===================================\n")

    client.close()


if __name__ == "__main__":
    main()
