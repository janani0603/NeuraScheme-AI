from pathlib import Path
import pandas as pd

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATASET = BASE_DIR / "dataset" / "government_schemes.csv"
OUTPUT_DATASET = BASE_DIR / "dataset" / "cleaned_government_schemes.csv"

print(f"Reading dataset:\n{RAW_DATASET}")

# -----------------------------
# Read CSV
# -----------------------------
df = pd.read_csv(RAW_DATASET)

print(f"\nOriginal Records : {len(df)}")

# -----------------------------
# Remove unnamed columns
# -----------------------------
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Remove completely empty column names
df = df.loc[:, df.columns != ""]

# -----------------------------
# Replace NaN
# -----------------------------
df = df.fillna("")

# -----------------------------
# Remove duplicate schemes
# -----------------------------
df = df.drop_duplicates(subset=["scheme_name"])

# -----------------------------
# Strip spaces
# -----------------------------
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].astype(str).str.strip()

# -----------------------------
# Clean scheme name
# -----------------------------
df["scheme_name"] = (
    df["scheme_name"]
    .str.replace('"', "", regex=False)
)

# -----------------------------
# Convert categories
# -----------------------------
def clean_categories(value):
    if value == "":
        return []

    return [
        x.strip().title()
        for x in value.split(",")
        if x.strip()
    ]

df["schemeCategory"] = df["schemeCategory"].apply(clean_categories)

# -----------------------------
# Convert tags
# -----------------------------
def clean_tags(value):
    if value == "":
        return []

    return [
        x.strip().title()
        for x in value.split(",")
        if x.strip()
    ]

df["tags"] = df["tags"].apply(clean_tags)

# -----------------------------
# Create search text
# -----------------------------
def build_search_text(row):

    text = " ".join([
        row["scheme_name"],
        row["details"],
        row["benefits"],
        row["eligibility"],
        " ".join(row["schemeCategory"]),
        " ".join(row["tags"])
    ])

    return text.lower()

df["search_text"] = df.apply(build_search_text, axis=1)

# -----------------------------
# Save cleaned CSV
# -----------------------------
df.to_csv(OUTPUT_DATASET, index=False)

print(f"\nCleaned Records : {len(df)}")
print(f"\nSaved cleaned dataset to:\n{OUTPUT_DATASET}")