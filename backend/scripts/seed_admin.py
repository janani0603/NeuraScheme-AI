"""
Create the first admin user.

Usage (from backend/ directory):
    venv\Scripts\python.exe scripts\seed_admin.py

You will be prompted for name, email, and password.
If the email already exists, the script upgrades that account to admin.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import os
import getpass
from pymongo import MongoClient
from datetime import datetime, UTC
from app.models.user import new_user_document
from app.auth.password import hash_password

MONGODB_URI   = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "neurascheme")

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

print("\n===================================")
print(" NeuraScheme AI — Seed Admin User")
print("===================================\n")

name     = input("Admin Name : ").strip()
email    = input("Admin Email: ").strip().lower()
password = getpass.getpass("Password   : ")

if len(password) < 8:
    print("❌ Password must be at least 8 characters.")
    sys.exit(1)

existing = db["users"].find_one({"email": email})

if existing:
    db["users"].update_one(
        {"email": email},
        {"$set": {"role": "admin", "updatedAt": datetime.now(UTC)}},
    )
    print(f"\n✅ Existing user '{email}' upgraded to admin.")
else:
    doc = new_user_document(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role="admin",
    )
    db["users"].insert_one(doc)
    print(f"\n✅ Admin user '{email}' created successfully.")

print("You can now log in at /login with these credentials.\n")
client.close()
