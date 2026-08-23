"""
Main Orchestration Pipeline Engine
Runs all 13 stages in strict order with progress updates and callback hooks for CLI / UI.
"""
import pandas as pd
from typing import Dict, Any, List, Optional, Callable
from src.ingest import load_and_validate_input
from src.cleaning import clean_record_placeholders
from src.dedup import process_deduplication
from src.resolution import resolve_manufacturer_and_brand
from src.taxonomy import classify_record
from src.retrieval import retrieve_enrichment_data
from src.extraction import extract_attributes_and_features
from src.normalization import normalize_record
from src.descriptions import generate_descriptions
from src.assets import resolve_digital_assets
from src.assembly import assemble_row_schema
from src.validation import validate_and_score_row
from src.evaluation import run_gold_row_regression, compute_dataset_metrics
from src.export import validate_and_export_deliverables

def run_enrichment_pipeline(
    input_source,
    mode: str = "auto",
    sample_size: Optional[int] = None,
    progress_callback: Optional[Callable[[int, str], None]] = None,
    export_csv: Optional[str] = None,
    export_xlsx: Optional[str] = None,
    export_qa: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes the full 13-stage UniHack AI Product Intelligence Enrichment Pipeline.
    """
    def log_progress(step: int, msg: str):
        if progress_callback:
            progress_callback(step, msg)

    # Stage 0: Ingest & Profile
    log_progress(0, "Stage 0: Ingesting & Profiling Input CSV...")
    df_raw = load_and_validate_input(input_source)
    if sample_size and sample_size > 0:
        df_raw = df_raw.head(sample_size)
    
    raw_records = df_raw.to_dict(orient="records")
    total = len(raw_records)

    # Stage 1: Placeholder Cleaning
    log_progress(1, "Stage 1: Cleaning placeholder brand strings...")
    cleaned_records = [clean_record_placeholders(r) for r in raw_records]

    # Stage 2: De-duplication & Alternate MPN resolution
    log_progress(2, "Stage 2: Processing de-duplication & alternate MPNs...")
    deduped_records = process_deduplication(cleaned_records)

    # Stage 3 to 11 per row
    log_progress(3, "Stage 3–11: Resolving manufacturers, taxonomy, enrichment, attributes, & assembly...")
    
    assembled_rows = []
    qa_sidecar_rows = []

    for idx, rec in enumerate(deduped_records):
        # Stage 3: Manufacturer/Brand Resolution
        r3 = resolve_manufacturer_and_brand(rec)
        
        # Stage 4: Classification/Taxonomy
        r4 = classify_record(r3)
        
        # Stage 5: Enrichment Retrieval
        r5, retrieved_text = retrieve_enrichment_data(r4, mode=mode)
        
        # Stage 6: Attribute Extraction
        r6, groundedness = extract_attributes_and_features(r5, retrieved_text=retrieved_text)
        
        # Stage 7: Normalization
        r7 = normalize_record(r6)
        
        # Stage 8: Description Generation
        r8 = generate_descriptions(r7)
        
        # Stage 9: Digital Assets
        r9 = resolve_digital_assets(r8)
        
        # Stage 10: Schema Assembly (Exact 252 header mapping)
        row_252 = assemble_row_schema(r9)
        assembled_rows.append(row_252)
        
        # Stage 11: Validation & Confidence Scoring
        conf_score, needs_review, reason = validate_and_score_row(row_252, groundedness=groundedness)
        qa_sidecar_rows.append({
            "row_index": idx + 1,
            "Mfg_Part_Num": row_252.get("Mfg_Part_Num", ""),
            "MANUFACTURER_NAME": row_252.get("MANUFACTURER_NAME", ""),
            "BRAND_NAME": row_252.get("BRAND_NAME", ""),
            "confidence_score": conf_score,
            "needs_human_review": needs_review,
            "review_reason": reason,
            "groundedness_score": groundedness
        })

    output_df = pd.DataFrame(assembled_rows)
    qa_df = pd.DataFrame(qa_sidecar_rows)

    # Stage 12: Evaluation Harness
    log_progress(12, "Stage 12: Running Gold-Row Regression & Dataset Metrics...")
    gold_regression = run_gold_row_regression(output_df)
    dataset_metrics = compute_dataset_metrics(output_df, qa_df)

    # Stage 13: Export
    if export_csv or export_xlsx or export_qa:
        log_progress(13, "Stage 13: Enforcing 252-header assertion and exporting deliverables...")
        c_path = export_csv if export_csv else "UniHack_Enriched_Product_Intelligence.csv"
        x_path = export_xlsx if export_xlsx else "UniHack_Enriched_Product_Intelligence.xlsx"
        q_path = export_qa if export_qa else "UniHack_QA_and_Evaluation_Report.csv"
        validate_and_export_deliverables(output_df, qa_df, csv_path=c_path, xlsx_path=x_path, qa_report_path=q_path)

    log_progress(13, "Pipeline execution completed successfully!")

    return {
        "output_df": output_df,
        "qa_df": qa_df,
        "gold_regression": gold_regression,
        "metrics": dataset_metrics
    }
