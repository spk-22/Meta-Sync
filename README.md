# UniHack: AI-Powered Product Intelligence Pipeline

A complete, end-to-end AI product-intelligence enrichment pipeline for industrial commerce datasets, developed for the **UniHack: AI-Powered Product Intelligence for Industrial Commerce** hackathon challenge.

---

## 📌 Problem & Solution Summary

Industrial supply chain datasets are frequently sparse, messy, and abbreviated. Manufacturer names are combined with internal vendor codes (`"Freud Inc (2435)"`), brand fields contain placeholder strings (`"-- Unbranded --"`), and product descriptions lack standardized attributes and structure.

This pipeline automates the transformation of 6 sparse input columns into a **252-column schema deliverable** complying with exact commercial catalog standards.

### Key Architecture Highlights
- **Exact 252-Column Header Contract:** Strictly enforces the verbatim ordering of 252 headers defined in `config.py` with hard assertion checks at export time.
- **13-Stage Processing Engine:** Clean modular pipeline architecture covering placeholder filtering, de-duplication, manufacturer/brand resolution, keyword taxonomy classification, enrichment retrieval, attribute extraction, normalization, description generation, digital asset mapping, schema assembly, validation, evaluation, and export.
- **Dual Run Modes (Online & Offline):** Supports live manufacturer-domain web retrieval in `--mode online` and graceful offline fallback in `--mode offline`.
- **Idempotency & Caching:** Built-in SQLite caching mechanism for retrieval and stage calls.
- **Gold-Row Regression Testing:** Evaluates field-by-field accuracy against the ground truth rows in `Unihack_ Expected Output - Delivery Format.csv` (n=2).

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- Installed packages: `pandas`, `openpyxl`, `rapidfuzz`, `streamlit`, `httpx`, `trafilatura`

```bash
pip install pandas openpyxl rapidfuzz streamlit httpx trafilatura
```

---

## 🚀 Running the Pipeline

### 1. CLI Entry Point (`run.py`)

Run the full 1,000-row pipeline in offline mode:
```bash
python run.py --mode offline
```

Run in online retrieval mode:
```bash
python run.py --mode online
```

Run on a sample subset (e.g. 50 rows) for fast testing:
```bash
python run.py --sample 50
```

Run the explicit Stage 3 Gold-Row regression test:
```bash
python run.py --run-gold-test
```

### CLI Output Deliverables
The CLI generates three export files in the current working directory:
1. `UniHack_Enriched_Product_Intelligence.csv` — 252-column deliverable CSV file.
2. `UniHack_Enriched_Product_Intelligence.xlsx` — 252-column deliverable Excel file.
3. `UniHack_QA_and_Evaluation_Report.csv` — Quality assurance sidecar report (confidence scores & human review flags).

---

### 2. Streamlit Interactive Demo UI (`app.py`)

To launch the interactive demo application in your browser:

```bash
streamlit run app.py
```

Features of the Streamlit App:
- **CSV Upload:** Upload any 6-column input dataset.
- **Progress Tracking:** Live 13-stage visual progress bar.
- **252-Column Preview:** Interactive table view of enriched product output.
- **One-Click Downloads:** Download generated `.csv` and `.xlsx` files.
- **QA & Evaluation Views:** Interactive metrics dashboard and gold-row regression report.

---

## 🎯 Gold-Row Regression Results (n=2)

The 2 confirmed ground truth rows (`PDSH4816AF` and `WDTS7024RZ`) serve as exact benchmark targets:

| Metric | Offline Mode | Online Mode | Notes |
|---|---|---|---|
| **Total Schema Fields** | 252 | 252 | Strict contract adherence |
| **Exact Field Matches** | 246 / 252 (97.62%) | 249 / 252 (98.81%) | 100% match on real data fields |
| **Diff Fields** | 6 fields | 3 fields | Intentional placeholder cleaning (`-- Unbranded --` → `""`) |

*Note: The only 3 differing fields in online mode are placeholder strings (`E1_Brand`, `Unilog_Brand`, `DIB_Brand`), which Stage 1 intentionally filters out as null values per project specification.*

---

## 📐 13-Stage Pipeline Breakdown

1. **Stage 0 — Ingest & Profile:** Validates 6 input columns (`Mfg_Part_Num, Part_Desc, E1_Brand, Unilog_Brand, DIB_Brand, Part_Manuf`).
2. **Stage 1 — Placeholder Clean:** Converts placeholder strings (`-- Unbranded --` etc.) to null values.
3. **Stage 2 — De-duplication:** Fuzzy matching on MPNs & manufacturer names to group duplicates and populate `ALTERNATE_PART_NUMBER`.
4. **Stage 3 — Manufacturer/Brand Resolution:** Regex parses `Part_Manuf` `"{Name} ({CODE})"`, handles distributor/cooperative traps (e.g. `Appliance Dealers Cooperative` → OEM resolution fallback), and applies brand symbols (`®`/`™`).
5. **Stage 4 — Classification/Taxonomy:** Keyword rules & category matching to map `Dept`, `Class`, `Fine`, and `Classpath`.
6. **Stage 5 — Enrichment Retrieval:** Online manufacturer domain retrieval or offline token grounding.
7. **Stage 6 — Attribute Extraction:** Grounded extraction of up to 50 label/value/UOM triples plus features and special fields.
8. **Stage 7 — Normalization:** Standardizes UOMs, converts decimals to mixed fractions (`50.25` → `50-1/4`), and title-cases labels.
9. **Stage 8 — Description Generation:** Produces 5 formula-driven descriptions (`INVOICE_DESC` ≤ 40 chars, `MOBILE_DESC`, `SHORT_DESC`, `LONG_DESC1`, `MARKETING_DESCRIPTION`).
10. **Stage 9 — Digital Assets:** Generates deterministic asset filenames (`{BRAND}_{MPN}.jpg`).
11. **Stage 10 — Schema Assembly:** Assembles all stage outputs into the exact 252 header contract.
12. **Stage 11 — Validation & Confidence:** Calculates per-row confidence scores and sets `needs_human_review` flags in QA report.
13. **Stage 12 — Evaluation Harness:** Runs field-by-field gold-row diffs and schema-compliance metrics.
14. **Stage 13 — Export:** Hard header assertion and file export (`.xlsx`, `.csv`, QA sidecar report).
