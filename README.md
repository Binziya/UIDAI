# 🆔 Biometric Stability Index (BSI) – Aadhaar Update Intelligence System

Monitoring biometric stability to prevent service inactivation and improve Aadhaar service delivery.

## Hackathon Details
- **Hackathon:** UIDAI Data Hackathon 2026  
- **Team ID:** UIDAI_5986  
- **Problem Owner:** Unique Identification Authority of India (UIDAI)

## Team Members
- Binziya  
- Sidhendra  
- Karthik  
- Nashva Jabbar  
- Rasna Faiza  

---

## Project Overview

Aadhaar enrolment and biometric update data contains valuable insights, but in its raw form it is not suitable for decision-making.  
This project introduces the **Biometric Stability Index (BSI)** — a decision-support metric that converts raw enrolment and update data into actionable geographic insights.

The system helps UIDAI proactively identify regions where biometric instability or service accessibility issues may lead to authentication failures.

---

## Problem Statement

UIDAI currently addresses biometric issues reactively, often after a citizen fails authentication.

Key challenges:
- **Visibility Gap (Low Update Areas):**  
  Low activity for adults may indicate stable biometrics otherwise lack of awareness/access.
- **Reliability Gap (High Update Areas):**  
  Adult biometrics usually around 25 should be stable; high update frequency may indicate biometric degradation or technical mismatch. As the dataset includes a combined 17+ category, unusually high update frequency in this group likely reflects non-biological causes and warrants targeted regional analysis.
---

## Solution Approach

The **Biometric Stability Index (BSI)** measures biometric health by analyzing update frequency against the enrolled population.

The model:
- Filters data age-wise to avoid biological bias
- Focuses on adult biometric stability (17+)
- Flags regions needing awareness, access, or technical intervention

---

## Key Metric – Biometric Stability Index (BSI)

**BSI = (Number of Biometric Updates) / (Total Enrolled Population)**  
Calculated at state, district, and pincode levels.

### Age-Based Segmentation
- **Adults (17+):** Primary focus group  
- **Adolescents (5–17):** Control group for natural biometric changes

---

## Datasets Used

1. Aadhaar Enrolment Dataset  
   - Age groups: 0–5, 5–17, 18+  
   - Spatial and temporal coverage  

2. Aadhaar Biometric Update Dataset  
   - Fingerprint, Iris, Face updates  

All datasets are anonymized and aggregated.

---

## Methodology

- Data cleaning and validation
- Age-wise segmentation
- Regional aggregation (State → District → Pincode)
- BSI calculation
- Dashboard visualization with threshold-based alerts

---

## Dashboard Features

- Pincode-wise update tracking
- Adult vs adolescent comparison
- Stability threshold (BSI = 2.0)
- Hotspot identification
- Automated recommendations

---

## Tech Stack

- Python  
- Pandas  
- Streamlit  
- Plotly Express  
- CSV (UIDAI datasets)

---

## Recommendations

- Conduct surveys in high-BSI regions
- Deploy mobile awareness camps in low-BSI regions
- Enhance future models with finer age segmentation

---

## Source Code

All analysis scripts and dashboard visualizations are included in this repository and are fully reproducible.

---

## Conclusion

The Biometric Stability Index (BSI) transforms Aadhaar biometric update data into a proactive monitoring tool, enabling UIDAI to identify service risks early and improve citizen experience.
