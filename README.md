# Meta Sync — AI-Powered Product Intelligence Pipeline

An end-to-end AI product-intelligence enrichment pipeline for industrial commerce datasets, developed for the **UniHack: AI-Powered Product Intelligence for Industrial Commerce** hackathon challenge.

🌐 Live Public Application Link
🔗 Public Dashboard Link: https://6f1b0ded8f282f51-171-76-83-60.serveousercontent.com

---

## 📌 Problem & Solution Overview

Industrial supply chain product catalogs are frequently sparse, messy, and abbreviated. Manufacturer names are combined with internal vendor codes (`"Freud Inc (2435)"`), brand fields contain placeholder strings (`"-- Unbranded --"`), and product descriptions lack standardized attributes and structure.

**Meta Sync** automates the transformation of sparse 6-column input datasets into a **literal 252-column schema deliverable** complying with exact commercial catalog standards.

---

## ✨ Key Features & Architecture Highlights

- **Literal 252-Column Header Contract:** Enforces verbatim ordering of all 252 delivery headers with hard assertion gates at export time.
- **13-Stage Processing Engine:** Ingest ➔ Placeholder Clean ➔ De-duplication ➔ OEM Resolution ➔ Taxonomy Classification ➔ Retrieval ➔ Attribute Extraction ➔ UOM Normalization ➔ 5x Description Engine ➔ Digital Assets ➔ 252 Assembly ➔ Validation ➔ Evaluation ➔ Export.
- **Visual Analytics Dashboard:** Built-in Streamlit dashboard featuring an interactive 13-stage methodology flowchart, Plotly analytics charts, 252-column data preview, and 1-click CSV/XLSX downloads.
- **Dual Run Modes:** Default `--mode offline` (100% self-contained local processing) and optional `--mode online` (domain-filtered search retrieval).
- **Quality Assurance Sidecar:** Generates a separate QA report (`UniHack_QA_and_Evaluation_Report.csv`) tracking confidence scores and `needs_human_review` flags without polluting the deliverable schema.
- **Un-hardcoded Evaluation Harness:** Evaluates field-by-field accuracy against ground truth gold rows (n=2).

---

## 📂 Repository Structure

```
Meta-Sync/
├── config.py                 # Literal 252 header constant, taxonomy rules, UOM maps
├── app.py                    # Streamlit visual analytics dashboard & flowchart
├── run.py                    # CLI entry point (--mode offline|online, --sample N)
├── requirements.txt          # Python dependencies
├── IMPLEMENTATION.md         # Detailed 13-stage technical implementation breakdown
├── RESULTS.md                # Full evaluation & benchmark metrics report
├── src/                      # Modular 13-stage pipeline package
│   ├── ingest.py             # Stage 0: Ingest & profile
│   ├── cleaning.py           # Stage 1: Placeholder clean & passthrough preservation
│   ├── dedup.py              # Stage 2: RapidFuzz de-duplication & alternate MPNs
│   ├── resolution.py         # Stage 3: OEM manufacturer & brand resolution
│   ├── taxonomy.py           # Stage 4: Category keyword taxonomy rules
│   ├── retrieval.py          # Stage 5: Enrichment retrieval (online & offline)
│   ├── extraction.py         # Stage 6: Grounded attribute & feature extraction
│   ├── normalization.py      # Stage 7: UOM dictionary & decimal ↔ fraction converter
│   ├── descriptions.py       # Stage 8: 5x formulaic description engine
│   ├── assets.py             # Stage 9: Digital asset filename generator
│   ├── assembly.py           # Stage 10: 252-column schema assembly
│   ├── validation.py         # Stage 11: Validation & confidence sidecar scoring
│   ├── evaluation.py         # Stage 12: Gold-row diff harness & batch metrics
│   ├── export.py             # Stage 13: Hard header assertion & file export
│   └── cache.py              # SQLite local caching engine
└── deliverables/             # Generated output deliverables (.csv, .xlsx, QA report)
```

---

## 🚀 Quick Start Guide

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run Pipeline via CLI (`run.py`)
Run the full 1,000-row pipeline in offline mode (default):
```bash
python run.py --mode offline
```

Run on a sample subset (e.g. 20 rows):
```bash
python run.py --sample 20
```

Run the Stage 3 Gold-Row unit test:
```bash
python run.py --run-gold-test
```

### 3. Launch Interactive Web Dashboard (`app.py`)
```bash
streamlit run app.py
```

---

## 📊 Evaluation & Benchmark Highlights

- **Schema Contract Compliance:** 252 / 252 Columns (100% Assertion Passed)
- **Gold-Row Benchmark Match Rate:** 207 / 252 fields (82.14% match rate on `PDSH4816AF`), 198 / 252 fields (78.57% match rate on `WDTS7024RZ`) — 100% un-hardcoded dynamic generation.
- **Passthrough Preservation:** `E1_Brand`, `Unilog_Brand`, `DIB_Brand` match ground truth **100%**.
- **Description Compliance:** 100% char-limit compliance for `INVOICE_DESC` (≤ 40 chars) and `MOBILE_DESC` (≤ 80 chars).

For full benchmark details, see [`RESULTS.md`](file:///d:/meta%20sync/RESULTS.md) and [`IMPLEMENTATION.md`](file:///d:/meta%20sync/IMPLEMENTATION.md).
