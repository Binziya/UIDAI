import pandas as pd

# -------------------------------
# 1. Load input Excel file (Task 3)
# -------------------------------
df = pd.read_excel("OUTPUT/task3_risk_output.xlsx")
df["date"] = pd.to_datetime(df["date"], dayfirst=True)
# -------------------------------
# 2. Define relative thresholds
# -------------------------------
LOW_BSI = df[["BSI_5_17", "BSI_17_plus"]].quantile(0.25).mean()
HIGH_BSI = df[["BSI_5_17", "BSI_17_plus"]].quantile(0.75).mean()

# -------------------------------
# 3. Default columns
# -------------------------------
df["Focus_Area"] = "Normal"
df["Recommended_Action"] = "No Immediate Action"

# -------------------------------
# 4. LOW frequency → Awareness / Access gap
# -------------------------------
low_freq = (
    (df["BSI_5_17"] < LOW_BSI) &
    (df["BSI_17_plus"] < LOW_BSI)
)

df.loc[low_freq, "Focus_Area"] = "Low Update Frequency"
df.loc[low_freq, "Recommended_Action"] = (
    "Conduct awareness campaigns and improve update center accessibility"
)

# -------------------------------
# 5. HIGH frequency (5–17) → Biological
# -------------------------------
high_5_17 = (
    (df["BSI_5_17"] > HIGH_BSI) &
    (df["BSI_17_plus"] <= HIGH_BSI)
)

df.loc[high_5_17, "Focus_Area"] = "High Updates (5–17)"
df.loc[high_5_17, "Recommended_Action"] = (
    "Plan periodic biometric update camps due to growth-related changes"
)

# -------------------------------
# 6. HIGH frequency (17+) → Instability risk
# -------------------------------
high_17_plus = df["BSI_17_plus"] > HIGH_BSI

df.loc[high_17_plus, "Focus_Area"] = "High Updates (17+)"
df.loc[high_17_plus, "Recommended_Action"] = (
    "Priority biometric review, device quality check, and targeted update camps"
)

# -------------------------------
# 7. Time-interval gap analysis
# -------------------------------
df = df.sort_values(by=["state", "district", "pincode", "date"])

df["Update_Gap_Days"] = (
    df.groupby(["state", "district", "pincode"])["date"]
    .diff()
    .dt.days
)

# Flag frequent re-updates (< 180 days)
df["Repeated_Update_Flag"] = df["Update_Gap_Days"] < 180

df.loc[df["Repeated_Update_Flag"], "Recommended_Action"] += (
    " | Schedule repeated camps based on short update intervals to prevent failures"
)

# -------------------------------
# 8. Save final action plan to Excel
# -------------------------------
df.to_excel("OUTPUT/ABS_SRIS_Final_Action_Plan.xlsx", index=False)

print("ABS-SRIS action plan generated successfully in Excel.")