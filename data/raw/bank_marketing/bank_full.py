import pandas as pd

# -----------------------------
# 1. Read the CSV file
# -----------------------------
df = pd.read_csv("bank-full.csv", sep=";")

# -----------------------------
# 2. Basic Cleaning
# -----------------------------

df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

df = df.drop_duplicates()

df = df.dropna(how="all")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# -----------------------------
# 3. Convert categorical to numeric
# -----------------------------

if "y" in df.columns:
    df["y"] = df["y"].map({"yes": 1, "no": 0})

# Convert categorical columns to numeric codes
cat_cols = df.select_dtypes(include=["object", "string"]).columns

for col in cat_cols:
    df[col] = df[col].astype("category").cat.codes


# -----------------------------
# 4. Save cleaned CSV
# -----------------------------
df.to_csv("bank-full-clean.csv", index=False)

print("Cleaning completed and saved as bank-full-clean.csv")
