<<<<<<< HEAD
import pandas as pd
import os
import glob

# ================================
# PATHS
# ================================
BIO_DIR = "uidai/biometric_update"
ENR_DIR = "uidai/enrolment"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================================
# HELPER FUNCTION
# ================================
def load_files(folder):
    return (
        glob.glob(os.path.join(folder, "*.csv")) +
        glob.glob(os.path.join(folder, "*.xlsx"))
    )

# ================================
# LOAD & CLEAN BIOMETRIC DATA
# ================================
bio_files = load_files(BIO_DIR)

if not bio_files:
    raise FileNotFoundError("❌ No biometric update files found")

print("📂 Biometric files:")
for f in bio_files:
    print(" -", f)

bio_frames = []

for file in bio_files:
    df = pd.read_csv(file) if file.endswith(".csv") else pd.read_excel(file)

    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "bio_age_5_17": "bio_5_17",
        "bio_age_17_": "bio_17_plus"
    })

    required_cols = {
        "date", "state", "district", "pincode",
        "bio_5_17", "bio_17_plus"
    }

    missing = required_cols - set(df.columns)
    if missing:
        print(f"⚠ Skipping {file} (missing {missing})")
        continue

    df = df[list(required_cols)]
    df.fillna(0, inplace=True)

    bio_frames.append(df)

if not bio_frames:
    raise ValueError("❌ No valid biometric data loaded")

bio = pd.concat(bio_frames, ignore_index=True)

bio_clean = bio.groupby(
    ["date", "state", "district", "pincode"],
    as_index=False
).sum()

bio_clean.to_csv(f"{OUTPUT_DIR}/task1_clean_biometric.csv", index=False)
print("✅ Biometric data cleaned")

# ================================
# LOAD & CLEAN ENROLMENT DATA
# ================================
enr_files = load_files(ENR_DIR)

if not enr_files:
    raise FileNotFoundError("❌ No enrolment files found")

print("\n📂 Enrolment files:")
for f in enr_files:
    print(" -", f)

enr_frames = []

for file in enr_files:
    df = pd.read_csv(file) if file.endswith(".csv") else pd.read_excel(file)

    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "age_0_5": "enr_0_5",
        "age_5_17": "enr_5_17",
        "age_18_greater": "enr_18_plus"
    })

    required_cols = {
        "date", "state", "district", "pincode",
        "enr_0_5", "enr_5_17", "enr_18_plus"
    }

    missing = required_cols - set(df.columns)
    if missing:
        print(f"⚠ Skipping {file} (missing {missing})")
        continue

    df = df[list(required_cols)]
    df.fillna(0, inplace=True)

    enr_frames.append(df)

if not enr_frames:
    raise ValueError("❌ No valid enrolment data loaded")

enr = pd.concat(enr_frames, ignore_index=True)

enr_clean = enr.groupby(
    ["date", "state", "district", "pincode"],
    as_index=False
).sum()

enr_clean.to_csv(f"{OUTPUT_DIR}/task1_clean_enrolment.csv", index=False)
print("✅ Enrolment data cleaned")

# ================================
# MERGE & BSI CALCULATION
# ================================
merged = pd.merge(
    bio_clean,
    enr_clean,
    on=["date", "state", "district", "pincode"],
    how="inner"
)

merged["BSI_5_17"] = merged["bio_5_17"] / merged["enr_5_17"]
merged["BSI_17_plus"] = merged["bio_17_plus"] / merged["enr_18_plus"]

merged.replace([float("inf")], 0, inplace=True)
merged.fillna(0, inplace=True)

merged.to_csv(f"{OUTPUT_DIR}/task2_bsi_output.csv", index=False)

print("\n🎯 TASK-1 & TASK-2 COMPLETED SUCCESSFULLY")
=======
import pandas as pd
import os
import glob

# ================================
# PATHS
# ================================
BIO_DIR = "uidai/biometric_update"
ENR_DIR = "uidai/enrolment"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================================
# HELPER FUNCTION
# ================================
def load_files(folder):
    return (
        glob.glob(os.path.join(folder, "*.csv")) +
        glob.glob(os.path.join(folder, "*.xlsx"))
    )

# ================================
# LOAD & CLEAN BIOMETRIC DATA
# ================================
bio_files = load_files(BIO_DIR)

if not bio_files:
    raise FileNotFoundError("❌ No biometric update files found")

print("📂 Biometric files:")
for f in bio_files:
    print(" -", f)

bio_frames = []

for file in bio_files:
    df = pd.read_csv(file) if file.endswith(".csv") else pd.read_excel(file)

    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "bio_age_5_17": "bio_5_17",
        "bio_age_17_": "bio_17_plus"
    })

    required_cols = {
        "date", "state", "district", "pincode",
        "bio_5_17", "bio_17_plus"
    }

    missing = required_cols - set(df.columns)
    if missing:
        print(f"⚠ Skipping {file} (missing {missing})")
        continue

    df = df[list(required_cols)]
    df.fillna(0, inplace=True)

    bio_frames.append(df)

if not bio_frames:
    raise ValueError("❌ No valid biometric data loaded")

bio = pd.concat(bio_frames, ignore_index=True)

bio_clean = bio.groupby(
    ["date", "state", "district", "pincode"],
    as_index=False
).sum()

bio_clean.to_csv(f"{OUTPUT_DIR}/task1_clean_biometric.csv", index=False)
print("✅ Biometric data cleaned")

# ================================
# LOAD & CLEAN ENROLMENT DATA
# ================================
enr_files = load_files(ENR_DIR)

if not enr_files:
    raise FileNotFoundError("❌ No enrolment files found")

print("\n📂 Enrolment files:")
for f in enr_files:
    print(" -", f)

enr_frames = []

for file in enr_files:
    df = pd.read_csv(file) if file.endswith(".csv") else pd.read_excel(file)

    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "age_0_5": "enr_0_5",
        "age_5_17": "enr_5_17",
        "age_18_greater": "enr_18_plus"
    })

    required_cols = {
        "date", "state", "district", "pincode",
        "enr_0_5", "enr_5_17", "enr_18_plus"
    }

    missing = required_cols - set(df.columns)
    if missing:
        print(f"⚠ Skipping {file} (missing {missing})")
        continue

    df = df[list(required_cols)]
    df.fillna(0, inplace=True)

    enr_frames.append(df)

if not enr_frames:
    raise ValueError("❌ No valid enrolment data loaded")

enr = pd.concat(enr_frames, ignore_index=True)

enr_clean = enr.groupby(
    ["date", "state", "district", "pincode"],
    as_index=False
).sum()

enr_clean.to_csv(f"{OUTPUT_DIR}/task1_clean_enrolment.csv", index=False)
print("✅ Enrolment data cleaned")

# ================================
# MERGE & BSI CALCULATION
# ================================
merged = pd.merge(
    bio_clean,
    enr_clean,
    on=["date", "state", "district", "pincode"],
    how="inner"
)

merged["BSI_5_17"] = merged["bio_5_17"] / merged["enr_5_17"]
merged["BSI_17_plus"] = merged["bio_17_plus"] / merged["enr_18_plus"]

merged.replace([float("inf")], 0, inplace=True)
merged.fillna(0, inplace=True)

merged.to_csv(f"{OUTPUT_DIR}/task2_bsi_output.csv", index=False)

print("\n🎯 TASK-1 & TASK-2 COMPLETED SUCCESSFULLY")
>>>>>>> 8951cd275b94f6ed46eac16e62218405d0d9fb8e
print("📁 Output folder:", OUTPUT_DIR)