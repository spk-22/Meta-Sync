# Meta Sync — Pipeline Implementation Architecture

This document provides a technical deep-dive into the 13-stage architecture of **Meta Sync**, built for the *UniHack: AI-Powered Product Intelligence for Industrial Commerce* hackathon challenge.

---

## 📌 Architecture Overview

Meta Sync transforms sparse, 6-column raw product rows into a **literal 252-column delivery format schema** complying with industrial catalog standards.

```
Stage 0  Ingest & Profile        — Load CSV, validate 6 input columns present
Stage 1  Placeholder Clean       — "-- Unbranded --" → null (internal), preserve passthroughs
Stage 2  De-duplication          — RapidFuzz matching on MPN + parsed manufacturer name
Stage 3  OEM Resolution          — Part_Manuf regex parse + distributor/cooperative trap detector
Stage 4  Classification/Taxonomy — Category keyword rules (Dept > Class > Fine > Classpath)
Stage 5  Enrichment Retrieval    — Online search & domain filter; offline token fallback
Stage 6  Attribute Extraction    — Grounded regex & pattern extractors (Voltage, Size, Sound, etc.)
Stage 7  Normalization           — UOM standard dictionary, decimal to mixed fraction (50.25 → 50-1/4)
Stage 8  Description Engine      — 5 formulaic copy generators (INVOICE_DESC ≤40 chars, MOBILE_DESC ≤80)
Stage 9  Digital Assets          — Deterministic filename patterns ({BRAND}_{MPN}.jpg)
Stage 10 Schema Assembly         — Map fields into exact 252-column header contract
Stage 11 Validation & Confidence — Per-field checks, confidence score, needs_human_review sidecar
Stage 12 Evaluation Harness      — Gold-row diff (n=2) + full 1,000-row batch metrics
Stage 13 Export                  — Hard 252 header assertion + XLSX, CSV, QA report export
```

---

## 🔬 Stage-by-Stage Technical Details

### Stage 0 — Ingest & Profile ([`src/ingest.py`](file:///d:/meta%20sync/src/ingest.py))
- Validates the presence of required input columns: `Mfg_Part_Num`, `Part_Desc`, `E1_Brand`, `Unilog_Brand`, `DIB_Brand`, `Part_Manuf`.
- Strips whitespace and handles `NaN`/`None` values.

### Stage 1 — Placeholder Cleaning ([`src/cleaning.py`](file:///d:/meta%20sync/src/cleaning.py))
- Filters out placeholder strings (`-- Unbranded --`, `-- No Unilog Brand --`, `-- No DIB Brand --`, `-`, `NONE`, `N/A`).
- **Passthrough Preservation:** Retains raw input string columns (`E1_Brand`, `Unilog_Brand`, `DIB_Brand`, etc.) intact for Stage 10 schema export, storing cleaned tokens in internal `_clean_*` variables for pipeline logic.

### Stage 2 — De-duplication ([`src/dedup.py`](file:///d:/meta%20sync/src/dedup.py))
- Performs fuzzy string matching (`rapidfuzz.fuzz.ratio`) across MPNs and clean manufacturer names.
- Group near-duplicates (similarity ≥ 90%) and populates `ALTERNATE_PART_NUMBER` with equivalent spellings.

### Stage 3 — Manufacturer & Brand Resolution ([`src/resolution.py`](file:///d:/meta%20sync/src/resolution.py))
- Regex parses `Part_Manuf` as `^(.*)\s\(([A-Za-z0-9_-]+)\)\s*$` (e.g. `"Freud Inc (2435)"` → Name `"Freud Inc"`, Code `"2435"`).
- **Cooperative/Distributor Trap Detector:** Flags names containing `"Cooperative"`, `"Dealers"`, `"Distributors"`, `"Supply"` (e.g. `Appliance Dealers Cooperative`).
- **OEM Fallback Resolution:** Resolves true OEM manufacturer & brand from MPN prefix rules and description tokens (e.g., `PDSH` → Rheem Manufacturing / FRIGIDAIRE®, `WDTS` → Whirlpool Corporation / Whirlpool®).
- **Brand Formatting:** Formats recognized major commercial brands with standard ® / ™ symbols.

### Stage 4 — Classification & Taxonomy ([`src/taxonomy.py`](file:///d:/meta%20sync/src/taxonomy.py))
- Keyword-based taxonomy dictionary mapping terms in `Part_Desc` to `Dept > Class > Fine` and `Classpath` (e.g. `dishwasher` → `Appliances & Consumer Electronics>Kitchen Appliances>Built-In Dishwashers`).

### Stage 5 — Enrichment Retrieval ([`src/retrieval.py`](file:///d:/meta%20sync/src/retrieval.py))
- **Offline Mode (Default):** Runs 100% self-contained locally without external HTTP calls.
- **Online Mode:** Performs domain-filtered search queries for manufacturer sites, strictly blocking marketplace sites (`amazon.com`, `ebay.com`, `homedepot.com`).

### Stage 6 — Attribute Extraction ([`src/extraction.py`](file:///d:/meta%20sync/src/extraction.py))
- Grounded regex and pattern extractors for up to 50 label/value/UOM triples:
  - **Voltage:** `r"(\d+)\s*V"` → `("Voltage Rating", val, "V")`
  - **Amperage:** `r"(\d+)\s*A"` → `("Amperage Rating", val, "A")`
  - **Sound Level:** `r"(\d+)\s*dBA"` → `("Sound Level", val, "dBA")`
  - **Mounting:** `Built-in`, `Leg`, `Undercounter`, `Wall`
  - **Dimensions:** `(\d+[-/\d.]*)\s*in\s*([HWD])`
  - **Special Fields:** `With`, `Standard/Approvals` (`ENERGY STAR`, `UL Listed`, `NSF`), `Product Name`.

### Stage 7 — Normalization ([`src/normalization.py`](file:///d:/meta%20sync/src/normalization.py))
- **UOM Dictionary:** Standardizes units (`inch`/`in.`/`"` → `in`, `volt`/`vac` → `V`, `amp` → `A`, `decibel` → `dBA`). Enforces single space between number and unit (`24 in`, never `24in`).
- **Decimal ↔ Mixed Fraction Converter:** Pure arithmetic converter rounding to nearest 1/64 (`50.25` → `50-1/4`, `33.4375` → `33-7/16`, `50.1875` → `50-3/16`).

### Stage 8 — Description Generation ([`src/descriptions.py`](file:///d:/meta%20sync/src/descriptions.py))
- `INVOICE_DESC`: ≤ 40 characters, ALL CAPS, compressed format.
- `MOBILE_DESC`: ~60–80 characters: `{Manufacturer/Brand}, {Product Name}, {Series}, {MPN}`.
- `SHORT_DESC`: `{BRAND}® [{Series}] {MPN} {Product Name} [With {feature}]`.
- `LONG_DESC1`: Sentence-style full copy generated from brand, product name, series, extracted attributes, and additional info.
- `RETAIL_DESC` & `MARKETING_DESCRIPTION`: Formatted marketing copy or grounded empty string.

### Stage 9 — Digital Assets ([`src/assets.py`](file:///d:/meta%20sync/src/assets.py))
- Generates deterministic filename patterns (`{BRAND}_{MPN}.jpg`, `{BRAND}_{MPN}_Specification_Sheet.pdf`).
- Sets `Actual Image (Yes/No)` flag.

### Stage 10 — Schema Assembly ([`src/assembly.py`](file:///d:/meta%20sync/src/assembly.py))
- Maps stage outputs into the exact 252 delivery format headers constant.
- Synthesizes stable integer `PART_NUMBER` and `SKU - MY_PART_NUMBER` if absent.

### Stage 11 — Validation & Confidence ([`src/validation.py`](file:///d:/meta%20sync/src/validation.py))
- Calculates per-row confidence score (0.0 to 1.0) and sets `needs_human_review` flags in the QA sidecar report.

### Stage 12 — Evaluation Harness ([`src/evaluation.py`](file:///d:/meta%20sync/src/evaluation.py))
- Performs field-by-field regression diff against ground truth gold rows (n=2).
- Calculates schema-compliance and non-blank coverage metrics across full batch runs.

### Stage 13 — Export ([`src/export.py`](file:///d:/meta%20sync/src/export.py))
- Enforces strict 252 header assertion gate (`assert list(output_df.columns) == DELIVERY_FORMAT_HEADERS`).
- Exports `.csv`, `.xlsx`, and separate `UniHack_QA_and_Evaluation_Report.csv`.
