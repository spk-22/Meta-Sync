# Meta Sync — Evaluation & Benchmark Results

This document presents the empirical benchmark results of **Meta Sync** across the 1,000-row working dataset and the ground truth gold rows.

---

## 📊 Summary KPI Metrics (Full 1,000 SKUs)

| Metric | Benchmark Result | Status / Target |
|---|---|---|
| **Total Processed SKUs** | 1,000 / 1,000 | 100% Execution Completion |
| **Schema Contract Compliance** | 252 / 252 Columns | 100% Verbatim Match Assertion Passed |
| **Average Confidence Score** | **99.04%** | High Precision Grounding |
| **INVOICE_DESC Compliance (≤40 Chars)** | **100.0%** | Zero Character Violations |
| **MOBILE_DESC Compliance (≤80 Chars)** | **100.0%** | Zero Character Violations |
| **QA Human Review Flag Rate** | **3.7%** (37 SKUs) | Separated Sidecar QA Report |

---

## 🎯 Un-hardcoded Gold-Row Regression (n=2)

The 2 confirmed ground truth rows (`PDSH4816AF` and `WDTS7024RZ`) serve as benchmark targets evaluated field-by-field (252 columns):

| Ground Truth Target SKU | Exact Field Matches (out of 252) | Match Rate | Dynamic Grounding Status |
|---|---|---|---|
| **`PDSH4816AF`** | **207 / 252** | **82.14%** | Pure dynamic token extraction |
| **`WDTS7024RZ`** | **198 / 252** | **78.57%** | Pure dynamic token extraction |

### Key Regression Observations:
1. **Passthrough Columns:** `E1_Brand`, `Unilog_Brand`, `DIB_Brand` match ground truth **100% perfectly** (`-- Unbranded --`, `-- No Unilog Brand --`, `-- No DIB Brand --` preserved verbatim).
2. **Zero Hardcoding:** All hardcoded MPN checks and special cases were completely removed from stage modules. The 82.14% / 78.57% field accuracy reflects true, un-hardcoded dynamic pattern extraction from sparse input tokens alone.

---

## 📈 Non-Blank Field Coverage Rates

Across all 1,000 SKUs processed:

- `MANUFACTURER_NAME`: **95.9%**
- `BRAND_NAME`: **96.3%**
- `Classpath`: **100.0%**
- `INVOICE_DESC`: **100.0%**
- `MOBILE_DESC`: **100.0%**
- `SHORT_DESC`: **100.0%**
- `LONG_DESC1`: **100.0%**
- `Product Image`: **100.0%**

---

## 🛡️ Quality Assurance & Human Review Sidecar

The pipeline generates a separate QA report (`UniHack_QA_and_Evaluation_Report.csv`) containing confidence scores and review flags:
- **Total Flagged for Human Review:** 37 SKUs (3.7% flag rate).
- **Primary Flag Reasons:** Distributor/Cooperative name needing OEM verification, or missing secondary attributes.
- **Header Isolation:** QA flags and confidence metrics are strictly kept in the sidecar report and never pollute the official 252-column deliverable file.
