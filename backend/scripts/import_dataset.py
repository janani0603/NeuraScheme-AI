from pathlib import Path
from datetime import datetime, UTC
import ast
import os

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import BulkWriteError
from tqdm import tqdm

# ============================================================
# Load Environment Variables
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGODB_URI:
    raise ValueError("❌ MONGODB_URI not found in .env")

if not DATABASE_NAME:
    raise ValueError("❌ DATABASE_NAME not found in .env")

# ============================================================
# MongoDB Connection
# ============================================================

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

collection = db["schemes"]

# ============================================================
# Dataset Path
# ============================================================

DATASET = BASE_DIR.parent / "dataset" / "cleaned_government_schemes.csv"

print("\n===================================")
print(" NeuraScheme AI Dataset Import")
print("===================================\n")

print(f"Dataset : {DATASET}")

if not DATASET.exists():
    raise FileNotFoundError(DATASET)

# ============================================================
# Read Dataset
# ============================================================

df = pd.read_csv(DATASET)

print(f"Records Found : {len(df)}")

# ============================================================
# Convert list columns
# ============================================================

def convert_list(value):

    if pd.isna(value):
        return []

    if isinstance(value, list):
        return value

    try:
        return ast.literal_eval(value)
    except Exception:
        return [
            item.strip()
            for item in str(value).split(",")
            if item.strip()
        ]

df["schemeCategory"] = df["schemeCategory"].apply(convert_list)
df["tags"] = df["tags"].apply(convert_list)

# ============================================================
# Drop old collection
# ============================================================

print("\nRemoving old collection...")

collection.drop()

print("Done.")

# ============================================================
# Prepare Documents
# ============================================================

documents = []

print("\nPreparing documents...")

for _, row in tqdm(df.iterrows(), total=len(df)):

    document = {

        "scheme_name": row["scheme_name"],

        "slug": row["slug"],

        "details": row["details"],

        "benefits": row["benefits"],

        "eligibility": row["eligibility"],

        "application": row["application"],

        "documents": row["documents"],

        "level": row["level"],

        "schemeCategory": row["schemeCategory"],

        "tags": row["tags"],

        "search_text": row["search_text"],

        "createdAt": datetime.now(UTC),

        "updatedAt": datetime.now(UTC)

    }

    documents.append(document)

print(f"\nPrepared {len(documents)} documents.")

# ============================================================
# Batch Insert
# ============================================================

BATCH_SIZE = 500

print("\nUploading to MongoDB...\n")

inserted = 0

try:

    for i in tqdm(range(0, len(documents), BATCH_SIZE)):

        batch = documents[i:i+BATCH_SIZE]

        result = collection.insert_many(batch)

        inserted += len(result.inserted_ids)

except BulkWriteError as e:

    print(e.details)

print(f"\nInserted {inserted} documents successfully.")

# ============================================================
# Create Indexes
# ============================================================

print("\nCreating indexes...")

collection.create_index([("slug", ASCENDING)], unique=True)

collection.create_index([("scheme_name", ASCENDING)])

collection.create_index([("level", ASCENDING)])

collection.create_index([("schemeCategory", ASCENDING)])

collection.create_index([("tags", ASCENDING)])

print("Basic indexes created.")

# ============================================================
# Create Text Index
# ============================================================

print("Creating text search index...")

collection.create_index([
    ("scheme_name", TEXT),
    ("details", TEXT),
    ("benefits", TEXT),
    ("eligibility", TEXT),
    ("search_text", TEXT)
])

print("Text index created.")

# ============================================================
# Summary
# ============================================================

print("\n===================================")
print(" Import Completed Successfully")
print("===================================")

print(f"Database   : {DATABASE_NAME}")
print(f"Collection : schemes")
print(f"Documents  : {inserted}")

client.close()