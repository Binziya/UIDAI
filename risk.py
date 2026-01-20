import pandas as pd
import os
import glob

# ==============================
# PATHS
# ==============================
BIO_DIR = "uidai/biometric_update"
ENR_DIR = "uidai/enrolment"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# HELPER FUNCTION
# ==============================
def load_files(folder):
    return glob.glob(os.path.join(folder, "*.csv")) + \
           glob.glob(os.path.join(folder, "*.xlsx"))

# ==============================
# LOAD & CLEAN BIOMETRIC DATA
# ==============================
bio_frames = []

for file in load_files(BIO_DIR):
    df = pd.read_csv(file) if file.endswith(".csv") else pd.read_excel(file)

    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "state": "state",
        "district": "district",
        "pincode": "pincode",
        "date": "date",
        "bio_age_5_17": "bio_5_17",
        "bio_age_17_plus": "bio_17_plus"
    })

    required = {"state", "district", "pincode", "date", "bio_5_17", "bio_17_plus"}
    if not required.issubset(df.columns):
        continue

    df = df[list(required)]
    df.fillna(0, inplace=True)

    bio_frames.append(df)

if not bio_frames:
    raise ValueError("❌ No valid biometric files found")

bio = pd.concat(bio_frames, ignore_index=True)

bio_clean = bio.groupby(
    ["state", "district", "pincode", "date"], as_index=False
).sum()

# ==============================
# LOAD & CLEAN ENROLMENT DATA
# ==============================
enr_frames = []

for file in load_files(ENR_DIR):
    df = pd.read_csv(file) if file.endswith(".csv") else pd.read_excel(file)

    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "state": "state",
        "district": "district",
        "pincode": "pincode",
        "date": "date",
        "age_5_17": "enr_5_17",
        "age_18_plus": "enr_18_plus"
    })

    required = {"state", "district", "pincode", "date", "enr_5_17", "enr_18_plus"}
    if not required.issubset(df.columns):
        continue

    df = df[list(required)]
    df.fillna(0, inplace=True)

    enr_frames.append(df)

if not enr_frames:
    raise ValueError("❌ No valid enrolment files found")

enr = pd.concat(enr_frames, ignore_index=True)

enr_clean = enr.groupby(
    ["state", "district", "pincode", "date"], as_index=False
).sum()

# ==============================
# MERGE DATA
# ==============================
merged = pd.merge(
    bio_clean,
    enr_clean,
    on=["state", "district", "pincode", "date"],
    how="inner"
)

# ==============================
# BSI CALCULATION
# ==============================
merged["bsi_5_17"] = merged["bio_5_17"] / merged["enr_5_17"]
merged["bsi_17_plus"] = merged["bio_17_plus"] / merged["enr_18_plus"]

merged.replace([float("inf")], 0, inplace=True)
merged.fillna(0, inplace=True)

# ==============================
# RISK CLASSIFICATION
# ==============================
def classify_risk(bsi):
    if bsi >= 1.0:
        return "High Risk"
    elif bsi >= 0.5:
        return "Medium Risk"
    else:
        return "Low Risk"

merged["risk_5_17"] = merged["bsi_5_17"].apply(classify_risk)
merged["risk_17_plus"] = merged["bsi_17_plus"].apply(classify_risk)

# ==============================
# SAVE OUTPUT
# ==============================
output_path = os.path.join(OUTPUT_DIR, "BSI_Risk_Output.xlsx")
merged.to_excel(output_path, index=False)

print("✅ Risk calculation completed")
print(f"📊 Output saved at: {output_path}")