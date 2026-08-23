# UniHack — AI-Powered Product Intelligence Pipeline
## Build-ready implementation plan (feed this directly to Antigravity / a code-generation agent)

---

## 0. Ground truth about what you actually have

Only three resources exist for this challenge — verified directly against the uploaded files, not assumed:

1. **Solution Guide** (text) — describes the problem and *mentions* seven reference files (content guidelines, UOM list, decimal/fraction table, manufacturer/brand master, LOV, faucets spec, fittings spec) plus a "200-item ground truth" file. **None of these were ever attached anywhere in this challenge.** The guide itself says: *"The relevant information from these references is already represented within the columns of the provided datasets, so you can use them as supporting resources rather than treating them as separate datasets to process."* Read that as permission, not an obstacle — you are meant to work from the two real files below.
2. **`Unihack__Sample_Dataset_-_Input.csv`** — real, confirmed: **1,000 rows, exactly 6 columns**: `Mfg_Part_Num, Part_Desc, E1_Brand, Unilog_Brand, DIB_Brand, Part_Manuf`.
3. **`Unihack__Expected_Output_-_Delivery_Format__1_.csv`** — real, confirmed: **252-column header row + 2 fully-populated data rows.** Those 2 rows are the only ground truth you have anywhere, and they are verified to be real rows that exist inside the 1,000-row input (matched by `Mfg_Part_Num = PDSH4816AF` and `WDTS7024RZ`).

**Do not let generated code try to load any of the seven named reference files or a "200-item" file. They don't exist in this environment; any `pd.read_excel("UniCat_...")`-style call is a build-breaking bug, not a missing-file inconvenience.**

Everything the missing files would have provided is rebuilt as **hand-authored rules + LLM grounding + optional live retrieval**, described stage-by-stage below.

---

## 1. Problem framing

- **Input:** sparse, abbreviated rows. Brand fields are frequently placeholders (`-- Unbranded --`, `-- No Unilog Brand --`, `-- No DIB Brand --`) — these mean "empty," not "this is the brand."
- **Output:** one row per input row, in the **exact 252-column schema** (Section 3), covering canonical manufacturer/brand, taxonomy, five differently-formatted descriptions, up to 50 attribute triples, dimensions, identifiers, and 20+ digital-asset link columns.
- **Constraint:** this is constrained generation, not free writing. Every value must trace back to the original description, a resolved manufacturer/brand, retrieved source text, or an explicit hand-authored rule — never invented. A fluent but hallucinated row scores zero.
- **Judged on:** exact-header compliance, whether output matches the 2 known-good rows where the same MPNs appear, format/char-limit compliance on the generated descriptions, and honest reporting of what couldn't be resolved.

---

## 2. Verified data facts (use these numbers directly in code and in your submission writeup)

Confirmed by direct inspection of the uploaded CSVs:

- **`Part_Manuf` carries a `"{Name} ({CODE})"` pattern in 959/1000 rows (95.9%)** — e.g. `"Freud Inc (2435)"`, `"Kichler Lighting (KICLI)"`, `"Black & Decker/dewlt (2585)"`, `"Appliance Dealers Cooperative (APPDE)"`. This is the primary, deterministic manufacturer-resolution signal. Parse it with regex `^(.*)\s\(([A-Za-z0-9]+)\)\s*$` before doing anything else. The remaining ~4% (literal `"-"` or no parenthetical) fall back to description-text inference.
- **`E1_Brand` is the placeholder `"-- Unbranded --"` in 799/1000 rows (79.9%).** In the other ~200 rows it's a real, usable brand hint (`TIMBERTECH`, `TREX`, `United Window & Door`) — treat non-placeholder values as a high-confidence prior, don't discard them.
- **Manufacturer/distributor trap, confirmed by the 2 gold rows:** `Part_Manuf = "Appliance Dealers Cooperative (APPDE)"` on both dishwasher rows, but the *true* `MANUFACTURER_NAME` is `"Rheem Manufacturing"` (brand Frigidaire) for one and `"Whirlpool Corporation"` for the other. A cooperative/distributor-sounding `Part_Manuf` name must trigger a fallback to MPN-pattern/description-based OEM resolution rather than being passed through as the manufacturer.
- **Category spread across the real 1,000 rows** (rough clustering by keyword, for scoping the "depth" categories): lighting/fixtures/switches (Kichler, Philips, Satco, Leviton), building materials/decking/fencing (Parksite/Trex/Azek/TimberTech, Boise Cascade), power tools/hardware (Milwaukee, DeWalt, Makita, Festool, Kreg), abrasives (Diablo/Freud, 3M, Mirka), appliances (dishwashers via the distributor-cooperative pattern above), plus a long tail (safety/eyewear, tape, electrical, misc.). **No faucets or pipe fittings exist in the real data** — don't build toward those categories even though the Solution Guide's worked example is a dishwasher (that example is representative of *format*, not of category scope).
- **The 2 gold rows are your only labeled data.** Use them as a hard regression test: feed their exact `Part_Desc` / `Part_Manuf` through your pipeline and diff the result against the known-correct 252-column row. This is small (n=2) but 100% real — report it as exactly that in your evaluation, not inflated into a larger accuracy claim.

---

## 3. THE OUTPUT CONTRACT — literal 252 headers, in order

This is the exact header row from the uploaded Expected Output CSV, character-for-character. Copy this as a Python list constant. **Never reorder, rename, retype, drop, or add to it — the export step must assert the output columns equal this list exactly, or fail the build.**

```python
DELIVERY_FORMAT_HEADERS = [
    "MFR URL", "Ref URL 1", "Ref URL 2", "Ref URL 3", "Ref URL 4", "Ref URL 5",
    "PART_NUMBER", "Dept", "Class", "Fine", "SKU - MY_PART_NUMBER", "Mfg_Part_Num",
    "Part_Desc", "E1_Brand", "Unilog_Brand", "DIB_Brand", "Part_Manuf",
    "MANUFACTURER_NAME", "BRAND_NAME", "TRADE_NAME", "MANUFACTURER_PART_NUMBER",
    "ALTERNATE_PART_NUMBER", "Classpath", "MOBILE_DESC", "INVOICE_DESC",
    "SHORT_DESC", "LONG_DESC1", "RETAIL_DESC", "MARKETING_DESCRIPTION",
    "ITEM_FEATURES_1", "ITEM_FEATURES_2", "ITEM_FEATURES_3", "ITEM_FEATURES_4",
    "ITEM_FEATURES_5", "ITEM_FEATURES_6", "ITEM_FEATURES_7", "ITEM_FEATURES_8",
    "ITEM_FEATURES_9", "ITEM_FEATURES_10", "ITEM_FEATURES_11", "ITEM_FEATURES_12",
    "ITEM_FEATURES_13", "ITEM_FEATURES_14", "ITEM_FEATURES_15", "ITEM_FEATURES_16",
    "ITEM_FEATURES_17", "ITEM_FEATURES_18", "ITEM_FEATURES_19", "ITEM_FEATURES_20",
    "With", "Standard/Approvals", "Prop 65", "Application", "Includes", "Product Name",
    "ATTRIBUTE_LABEL 1", "ATTRIBUTE_VALUE 1", "ATTRIBUTE_UOM 1",
    "ATTRIBUTE_LABEL 2", "ATTRIBUTE_VALUE 2", "ATTRIBUTE_UOM 2",
    "ATTRIBUTE_LABEL 3", "ATTRIBUTE_VALUE 3", "ATTRIBUTE_UOM 3",
    "ATTRIBUTE_LABEL 4", "ATTRIBUTE_VALUE 4", "ATTRIBUTE_UOM 4",
    "ATTRIBUTE_LABEL 5", "ATTRIBUTE_VALUE 5", "ATTRIBUTE_UOM 5",
    "ATTRIBUTE_LABEL 6", "ATTRIBUTE_VALUE 6", "ATTRIBUTE_UOM 6",
    "ATTRIBUTE_LABEL 7", "ATTRIBUTE_VALUE 7", "ATTRIBUTE_UOM 7",
    "ATTRIBUTE_LABEL 8", "ATTRIBUTE_VALUE 8", "ATTRIBUTE_UOM 8",
    "ATTRIBUTE_LABEL 9", "ATTRIBUTE_VALUE 9", "ATTRIBUTE_UOM 9",
    "ATTRIBUTE_LABEL 10", "ATTRIBUTE_VALUE 10", "ATTRIBUTE_UOM 10",
    "ATTRIBUTE_LABEL 11", "ATTRIBUTE_VALUE 11", "ATTRIBUTE_UOM 11",
    "ATTRIBUTE_LABEL 12", "ATTRIBUTE_VALUE 12", "ATTRIBUTE_UOM 12",
    "ATTRIBUTE_LABEL 13", "ATTRIBUTE_VALUE 13", "ATTRIBUTE_UOM 13",
    "ATTRIBUTE_LABEL 14", "ATTRIBUTE_VALUE 14", "ATTRIBUTE_UOM 14",
    "ATTRIBUTE_LABEL 15", "ATTRIBUTE_VALUE 15", "ATTRIBUTE_UOM 15",
    "ATTRIBUTE_LABEL 16", "ATTRIBUTE_VALUE 16", "ATTRIBUTE_UOM 16",
    "ATTRIBUTE_LABEL 17", "ATTRIBUTE_VALUE 17", "ATTRIBUTE_UOM 17",
    "ATTRIBUTE_LABEL 18", "ATTRIBUTE_VALUE 18", "ATTRIBUTE_UOM 18",
    "ATTRIBUTE_LABEL 19", "ATTRIBUTE_VALUE 19", "ATTRIBUTE_UOM 19",
    "ATTRIBUTE_LABEL 20", "ATTRIBUTE_VALUE 20", "ATTRIBUTE_UOM 20",
    "ATTRIBUTE_LABEL 21", "ATTRIBUTE_VALUE 21", "ATTRIBUTE_UOM 21",
    "ATTRIBUTE_LABEL 22", "ATTRIBUTE_VALUE 22", "ATTRIBUTE_UOM 22",
    "ATTRIBUTE_LABEL 23", "ATTRIBUTE_VALUE 23", "ATTRIBUTE_UOM 23",
    "ATTRIBUTE_LABEL 24", "ATTRIBUTE_VALUE 24", "ATTRIBUTE_UOM 24",
    "ATTRIBUTE_LABEL 25", "ATTRIBUTE_VALUE 25", "ATTRIBUTE_UOM 25",
    "ATTRIBUTE_LABEL 26", "ATTRIBUTE_VALUE 26", "ATTRIBUTE_UOM 26",
    "ATTRIBUTE_LABEL 27", "ATTRIBUTE_VALUE 27", "ATTRIBUTE_UOM 27",
    "ATTRIBUTE_LABEL 28", "ATTRIBUTE_VALUE 28", "ATTRIBUTE_UOM 28",
    "ATTRIBUTE_LABEL 29", "ATTRIBUTE_VALUE 29", "ATTRIBUTE_UOM 29",
    "ATTRIBUTE_LABEL 30", "ATTRIBUTE_VALUE 30", "ATTRIBUTE_UOM 30",
    "ATTRIBUTE_LABEL 31", "ATTRIBUTE_VALUE 31", "ATTRIBUTE_UOM 31",
    "ATTRIBUTE_LABEL 32", "ATTRIBUTE_VALUE 32", "ATTRIBUTE_UOM 32",
    "ATTRIBUTE_LABEL 33", "ATTRIBUTE_VALUE 33", "ATTRIBUTE_UOM 33",
    "ATTRIBUTE_LABEL 34", "ATTRIBUTE_VALUE 34", "ATTRIBUTE_UOM 34",
    "ATTRIBUTE_LABEL 35", "ATTRIBUTE_VALUE 35", "ATTRIBUTE_UOM 35",
    "ATTRIBUTE_LABEL 36", "ATTRIBUTE_VALUE 36", "ATTRIBUTE_UOM 36",
    "ATTRIBUTE_LABEL 37", "ATTRIBUTE_VALUE 37", "ATTRIBUTE_UOM 37",
    "ATTRIBUTE_LABEL 38", "ATTRIBUTE_VALUE 38", "ATTRIBUTE_UOM 38",
    "ATTRIBUTE_LABEL 39", "ATTRIBUTE_VALUE 39", "ATTRIBUTE_UOM 39",
    "ATTRIBUTE_LABEL 40", "ATTRIBUTE_VALUE 40", "ATTRIBUTE_UOM 40",
    "ATTRIBUTE_LABEL 41", "ATTRIBUTE_VALUE 41", "ATTRIBUTE_UOM 41",
    "ATTRIBUTE_LABEL 42", "ATTRIBUTE_VALUE 42", "ATTRIBUTE_UOM 42",
    "ATTRIBUTE_LABEL 43", "ATTRIBUTE_VALUE 43", "ATTRIBUTE_UOM 43",
    "ATTRIBUTE_LABEL 44", "ATTRIBUTE_VALUE 44", "ATTRIBUTE_UOM 44",
    "ATTRIBUTE_LABEL 45", "ATTRIBUTE_VALUE 45", "ATTRIBUTE_UOM 45",
    "ATTRIBUTE_LABEL 46", "ATTRIBUTE_VALUE 46", "ATTRIBUTE_UOM 46",
    "ATTRIBUTE_LABEL 47", "ATTRIBUTE_VALUE 47", "ATTRIBUTE_UOM 47",
    "ATTRIBUTE_LABEL 48", "ATTRIBUTE_VALUE 48", "ATTRIBUTE_UOM 48",
    "ATTRIBUTE_LABEL 49", "ATTRIBUTE_VALUE 49", "ATTRIBUTE_UOM 49",
    "ATTRIBUTE_LABEL 50", "ATTRIBUTE_VALUE 50", "ATTRIBUTE_UOM 50",
    "UPC", "EAN", "GTIN", "UNSPSC", "Warranty", "List Price", "Selling Qty",
    "Selling UOM", "Standard Packaging Information", "LENGTH", "LENGTH_UOM",
    "HEIGHT", "HEIGHT_UOM", "WIDTH", "WIDTH_UOM", "WEIGHT", "WEIGHT_UOM",
    "VOLUME", "VOLUME_UOM", "Product Image", "Alternate Image 1",
    "Alternate Image 2", "Alternate Image 3", "Alternate Image 4", "SDS", "SDS_1",
    "Warranty Information", "Catalog", "Specification Sheet",
    "Instruction/Installation Manual", "Service Manual", "Owners/User Manual",
    "Line Drawing", "MTR", "RoHS", "Full Engineering Drawing",
    "Energy Star Guide", "Technical Bulletin", "Submittal", "Compatibility Chart",
    "Size Chart", "Product Label/Insert", "Video Link", "Video Link 1",
    "Country Of Origin", "Discontinued", "Actual Image (Yes/No)",
]
assert len(DELIVERY_FORMAT_HEADERS) == 252
```

At export time:
```python
assert list(output_df.columns) == DELIVERY_FORMAT_HEADERS, "Header contract violated — build-breaking bug."
```

### Column-group → source-stage map

| Columns | Count | Fed by | Notes |
|---|---|---|---|
| `MFR URL`, `Ref URL 1-5` | 6 | Stage 5 | Only filled if retrieval actually ran and found a source; otherwise blank |
| `PART_NUMBER` | 1 | synthesized | Not present in real input; synthesize a stable ID (e.g. hash of MPN+manufacturer) and note it's synthetic |
| `Dept`, `Class`, `Fine` | 3 | Stage 4 | Never in the real input — always derived from `Part_Desc` |
| `SKU - MY_PART_NUMBER` | 1 | synthesized | Same as PART_NUMBER |
| `Mfg_Part_Num`…`Part_Manuf` | 6 | passthrough | Copied verbatim from input, unchanged |
| `MANUFACTURER_NAME`, `BRAND_NAME`, `TRADE_NAME` | 3 | Stage 3 | Canonical name/brand with correct symbols |
| `MANUFACTURER_PART_NUMBER`, `ALTERNATE_PART_NUMBER` | 2 | passthrough + Stage 2 | Alternate = any equivalent spelling found during dedup, else blank |
| `Classpath` | 1 | Stage 4 | `>`-delimited taxonomy path |
| `MOBILE_DESC`…`MARKETING_DESCRIPTION` | 5 | Stage 8 | Five description formats, own rules each |
| `ITEM_FEATURES_1..20` | 20 | Stage 8 / Stage 6 | Bullet-style features, from retrieved spec text or description tokens; blank if none found |
| `With`, `Standard/Approvals`, `Prop 65`, `Application`, `Includes`, `Product Name` | 6 | Stage 6/8 | Best-effort; blank if not resolvable |
| `ATTRIBUTE_LABEL/VALUE/UOM 1..50` | 150 | Stage 6 + Stage 7 | Extracted attributes, normalized units |
| `UPC`…`VOLUME_UOM` | 20 | Stage 5/6 | Identifiers + dimensions; leave blank rather than guess |
| `Product Image`…`Actual Image (Yes/No)` | ~30 | Stage 9 | Deterministic filename pattern + `Actual Image` flag set to `No` unless a real image URL was found |

---

## 4. Pipeline architecture (13 stages, each a pure `dict -> dict` or `df -> df` function)

```
Stage 0  Ingest & Profile        — load CSV, validate 6 input columns present
Stage 1  Placeholder Clean       — "-- Unbranded --" / "-- No X Brand --" → null
Stage 2  De-duplication          — fuzzy match on MPN + parsed manufacturer name
Stage 3  Manufacturer/Brand Res. — Part_Manuf code-parse (primary) + LLM/retrieval canonicalization (fallback)
Stage 4  Classification/Taxonomy — keyword rules (hand-authored from real clusters) + LLM fallback → Dept/Class/Fine/Classpath
Stage 5  Enrichment Retrieval    — manufacturer-site search+fetch when internet is available; else skipped (see 4.1)
Stage 6  Attribute Extraction    — LLM extraction grounded in retrieved text or Part_Desc tokens only, never invented
Stage 7  Normalization           — UOM standardization, decimal→fraction, casing/hyphenation rules
Stage 8  Description Generation  — 5 formula-driven formats (Invoice/Mobile/Short/Long/Marketing)
Stage 9  Digital Assets          — deterministic filename pattern; Actual Image flag
Stage 10 Schema Assembly         — map into the exact 252-column row
Stage 11 Validation & Confidence — per-field checks, confidence score, needs_human_review (side-car, NOT in the 252)
Stage 12 Evaluation Harness      — gold-row regression (n=2) + schema-compliance metrics across all 1,000 rows
Stage 13 Export                  — .xlsx + .csv with the exact header row, plus a separate QA report file
```

### 4.1 Two explicit run modes (important — do not build only the online path)

Build the pipeline to run in **either** mode, selected by a flag, so the demo works even without internet access in the execution environment:

- **`--mode online`** (preferred if available): Stage 5 performs real web search + page fetch against manufacturer domains only (block marketplaces/distributor sites per the Solution Guide's sourcing rule). Confidence scores are higher; `Ref URL`/`MFR URL` columns get populated.
- **`--mode offline`** (fallback, always works): Stage 5 is a no-op. Stage 6 grounds attribute extraction only in `Part_Desc` tokens + the LLM's own parametric knowledge of the named manufacturer/product line, with attribute-level confidence marked lower and `Ref URL`/`MFR URL` left blank. The pipeline must still produce a complete, schema-valid 252-column file in this mode — this is your guaranteed fallback if Antigravity's execution sandbox has no network access.

Detect capability automatically at startup (try one cheap HTTP request; catch and fall back) rather than requiring the user to know which mode to pick.

### 4.2 Batching, caching, and demo-scale controls (needed for a 1,000-row run)

- Add a `--sample N` flag to process only the first N rows (or a stratified sample across the clusters in Section 2) — use this for the **live demo**, and run the full 1,000 separately, ahead of time, saving the output file to disk.
- Batch LLM calls with `asyncio` + a concurrency limit (e.g. 5–10 in flight), not one synchronous call per row — 1,000 sequential calls will be far too slow for a hackathon demo window.
- Cache every LLM/retrieval call keyed by `(Mfg_Part_Num, Part_Manuf, stage_name)` to a local file (e.g. `sqlite` or a JSON cache) so re-running the pipeline during development doesn't re-spend calls or time on rows you've already processed.
- Log per-stage timing and per-row failures to the QA report so a stalled row doesn't silently hang the batch — wrap each row in try/except, record `needs_human_review = True` on failure, and continue.

---

## 5. Stage details

**Stage 1 — Placeholder cleaning.** Treat `-- Unbranded --`, `-- No Unilog Brand --`, `-- No DIB Brand --` (and any `-- ... --` pattern) as null, not as data, before any matching/prompting touches them.

**Stage 2 — De-duplication.** Fuzzy-match `Mfg_Part_Num` + parsed manufacturer name (from Stage 3's parse) using `rapidfuzz`; group near-duplicates and populate `ALTERNATE_PART_NUMBER` with equivalent spellings found in the group.

**Stage 3 — Manufacturer/brand resolution.**
1. Regex-parse `Part_Manuf` as `"{Name} ({CODE})"` — covers 95.9% of rows deterministically for the *parse* step.
2. Detect distributor/cooperative-looking names (heuristics: contains "Cooperative", "Dealers", "Distributors", "Supply", or is a known non-OEM pattern) and treat these as **not** the true manufacturer — fall back to inferring OEM from the MPN prefix pattern and/or `Part_Desc` text (grounded in the 2 gold rows' proven behavior: `Appliance Dealers Cooperative` → true OEM resolved via product-line knowledge).
3. Use `E1_Brand`/other brand fields as a cross-check when non-placeholder.
4. Canonicalize the resulting name/brand (legal suffix, ®/™ symbol) via LLM world-knowledge, refined with live lookup in online mode.
5. **Unit test this stage against the 2 gold rows before moving on** — it must reproduce `MANUFACTURER_NAME = "Rheem Manufacturing"` / `"Whirlpool Corporation"` and `BRAND_NAME = "FRIGIDAIRE®"` / `"Whirlpool®"` from the same `Part_Manuf` input both rows share.

**Stage 4 — Classification/taxonomy.** Hand-author a keyword-to-classpath dictionary from the clusters in Section 2 (lighting, building materials, power tools, abrasives, appliances) using terms visible in `Part_Desc`; LLM fallback classifies the long tail into a plausible `Dept > Class > Fine` / `Classpath`. Never depend on `Dept`/`Class`/`Fine` being present in input — they never are (confirmed, Section 2).

**Stage 5 — Enrichment retrieval.** Search the manufacturer's own site (using the resolved name from Stage 3) for the specific MPN; fetch and extract spec-sheet or product-page text. Hard-block marketplace/distributor domains. Record every URL actually used in `MFR URL`/`Ref URL 1-5`. Skipped entirely in offline mode (4.1).

**Stage 6 — Attribute extraction.** LLM extracts label/value/UOM triples **only from**: retrieved spec text (if available), `Part_Desc` tokens, or resolved manufacturer/brand/classpath — never free-invented. Normalize labels to Title Case, dedupe labels per item, cap at 50 triples. Report groundedness (what fraction of triples trace to retrieved text vs. description-only) honestly in the QA report.

**Stage 7 — Normalization.**
- UOM: hand-built compact dictionary covering forms observed in the 2 gold rows plus standard industrial abbreviations (`in, ft, V, A, W, dBA, lb, oz, kW-hr, hr, gal, psi, °F, °C`), always with a space between number and unit (`24 in`, never `24in`).
- Decimal↔fraction: pure function, round to nearest 1/64 and render as mixed fraction (`50.25` → `50-1/4`) — no lookup table needed, this is ~10 lines of arithmetic.
- Casing/hyphenation: Title Case for labels and product names; brand symbols (®/™) preserved exactly as resolved in Stage 3.

**Stage 8 — Description generation.** Five outputs, each reverse-engineered from the two confirmed gold rows plus the Solution Guide's worked example (both describe the same underlying pattern — treat them as one confirmed source):
- `INVOICE_DESC`: ≤40 characters, ALL CAPS, most compressed (e.g. `DISHWASHER LEG 5 SST 120V 15A 50-1/4IN`).
- `MOBILE_DESC`: ~60–80 characters, `Manufacturer Brand, ItemType, Series, MPN[, key attribute]`.
- `SHORT_DESC` (Product Title): `BRAND® [Series] MPN ItemType With [feature], [key attr 1], [key attr 2], [material]`.
- `LONG_DESC1`: full sentence-style, brand + item type + series + all major specced attributes with units, ending with an "Additional Information:" clause for secondary attributes.
- `MARKETING_DESCRIPTION` / `RETAIL_DESC`: shorter marketing-style copy; leave blank if no source material supports it (the Frigidaire gold row itself has `MARKETING_DESCRIPTION` blank — a legitimate blank is more credible than a fabricated one).
Validate every generated field against its character limit programmatically before writing to output.

**Stage 9 — Digital assets.** Deterministic filename pattern (`{BRAND}_{MPN}.jpg` observed in gold rows) for `Product Image`; set `Actual Image (Yes/No)` to `No` unless a real, retrieved image URL exists — never claim an image exists that wasn't actually found.

**Stage 10 — Schema assembly.** Map every stage's output into the exact 252-column row per Section 3's map. Any field with no resolved value is written as an empty string, not `None`/`NaN`/a placeholder string.

**Stage 11 — Validation & confidence.** Per-row confidence score (e.g. weighted from: manufacturer-resolution certainty, whether retrieval succeeded, char-limit compliance, attribute groundedness) plus a `needs_human_review` boolean. **Both are side-car columns in the QA report — never inserted into the official 252-column file.**

**Stage 12 — Evaluation harness.**
- Regression test: run the pipeline on the two gold `Part_Desc`/`Part_Manuf` inputs (pulled live from the 1,000-row file, not hardcoded), diff every one of the 252 fields against the known-correct gold row, report exact/partial/mismatch per field.
- Schema-compliance metrics across all 1,000 rows: % rows with non-blank `MANUFACTURER_NAME`, % rows with non-blank `Classpath`, % descriptions within char limits, average attribute count, % attributes grounded in retrieved text vs. description-only.
- Report both honestly — the n=2 regression is real but small; the 1,000-row metrics are breadth, not accuracy, since there's no larger labeled set.

**Stage 13 — Export.** Write `.xlsx` (via `openpyxl`/`XlsxWriter`) and `.csv`, with the header-equality assertion from Section 3 as a hard gate before writing. Write the QA report (confidence scores, review flags, evaluation metrics) as a separate file — never mixed into the 252-column deliverable.

---

## 6. Recommended tech stack

- **Language:** Python 3.11
- **Data handling:** `pandas`, `openpyxl`
- **Fuzzy matching:** `rapidfuzz`
- **LLM calls:** Anthropic API (Claude), structured/JSON output, `asyncio` batching + concurrency cap
- **Retrieval (online mode only):** a search API + `httpx`/`trafilatura` for fetch & text extraction; strict manufacturer-domain allow-list, explicit marketplace/distributor block-list
- **Caching:** local `sqlite` or JSON keyed by `(Mfg_Part_Num, Part_Manuf, stage_name)`
- **Orchestration:** plain Python stage functions composed in `run.py`
- **Output:** `openpyxl`/`XlsxWriter` for `.xlsx`, stdlib `csv` for `.csv`
- **Demo UI (recommended):** small Streamlit app — upload input → progress bar per stage → preview table → download button → embedded evaluation report. Use `--sample N` under the hood so the live demo stays fast; the full 1,000-row file is pre-generated and just displayed/downloaded.

---

## 7. Build order / milestones

1. **Hour 0–1:** Ingest both real CSVs; hardcode `DELIVERY_FORMAT_HEADERS` (Section 3) and extract the 2 gold test cases programmatically from the Expected Output file; write the header-equality unit test.
2. **Hour 1–3:** Stages 1–3 — placeholder cleaning, dedup, manufacturer/brand resolution. Implement the `Part_Manuf` regex parser + cooperative-trap detector first; get the Stage-3 regression test passing against both gold rows before moving on.
3. **Hour 3–5:** Stage 4 — hand-author the keyword-classification dictionary from the real clusters (lighting, power tools, building materials, abrasives, appliances); LLM fallback for the rest.
4. **Hour 5–8:** Stages 5–6 — build the offline mode first (guaranteed to work), then layer online retrieval on top. Get **one category fully working end-to-end** (recommend lighting: simplest attribute set) before scaling out.
5. **Hour 8–10:** Stages 7–8 — normalization + all 5 description formats; validate against the 2 gold rows until char-limit and casing compliance is ~100%.
6. **Hour 10–11:** Stages 9–10 — digital assets + full 252-column assembly.
7. **Hour 11–13:** Stages 11–12 — confidence scoring + evaluation harness; run the gold-row regression diff.
8. **Hour 13–15:** Run the full pipeline on all 1,000 rows (offline mode as the safety net, online mode if time/network allow); sanity-check output; build/polish the Streamlit demo with `--sample N`.
9. **Hour 15–16:** Package deliverables (Section 8); write the submission description — be upfront that the seven named reference files were never actually provided and explain how the pipeline compensates; rehearse the demo, leading with the gold-row regression numbers.

---

## 8. Final deliverables checklist

- ✅ **Problem alignment:** pipeline targets structured generation from limited inputs, accuracy/consistency, AI validation & enrichment, and batch scalability across 1,000 items.
- ✅ **Solution Guide followed:** placeholder filtering, source-grounded generation, manufacturer-source sourcing hierarchy, depth-first on categories that actually exist in the real data.
- ✅ **Sample data tested:** full 1,000-row run completed; the 2 confirmed gold rows used as a genuine regression test; schema-compliance metrics reported honestly in place of a larger labeled-accuracy score that doesn't exist.
- ⚠️ **Exact output headers:** enforced by a hard assertion at export time against the literal Section 3 list — treat any mismatch as build-breaking.
- ✅ **Correct file export:** `.xlsx` + `.csv`.
- ✅ **External links attached:** include the Solution Guide link in the submission description, and state plainly which reference files were never provided and how their role was rebuilt.
- **Differentiator:** the QA/confidence report and evaluation harness — most competing teams will submit plausible-looking, unvalidated output; you submit output *plus proof of where it's right and where it isn't*.

---

## 9. Key pitfalls to avoid

1. Don't hardcode or mock against only the sample rows — the pipeline must run dynamically on unseen evaluation data with the same 6-column shape but different values.
2. Don't let the LLM free-generate attribute values or descriptions ungrounded — always tie back to retrieved text, `Part_Desc` tokens, or an explicit rule.
3. Don't treat placeholder brand strings (`-- Unbranded --` etc.) as real data.
4. Don't build any runtime dependency on the seven named reference files or a "200-item" file — they were never provided.
5. Don't force-fill genuinely unknown fields (UNSPSC, Country of Origin) — blank + flagged beats a fabricated value; the gold rows themselves have legitimate blanks.
6. Don't scrape or cite marketplace/distributor sources — manufacturer-only, hard-blocked otherwise.
7. Don't skip the offline fallback — if the execution environment has no network access, the pipeline must still produce a complete, schema-valid file.
8. Don't run 1,000 sequential, uncached LLM calls in the live demo — batch, cache, and use `--sample N` for the live walkthrough while the full run is pre-generated.
9. Don't overstate the evaluation — report the 2-gold-row regression as exactly what it is (small but real), not as a large validated accuracy figure.
