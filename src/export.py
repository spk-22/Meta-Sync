"""
Stage 13: Export & Header Assertion
Enforces strict 252 header equality assertion before writing deliverables to .csv and .xlsx files.
Writes QA report as a separate sidecar file.
"""
import pandas as pd
from typing import Dict, Any, List
from config import DELIVERY_FORMAT_HEADERS

def validate_and_export_deliverables(
    output_df: pd.DataFrame,
    qa_sidecar_df: pd.DataFrame,
    csv_path: str = "UniHack_Enriched_Product_Intelligence.csv",
    xlsx_path: str = "UniHack_Enriched_Product_Intelligence.xlsx",
    qa_report_path: str = "UniHack_QA_and_Evaluation_Report.csv"
) -> None:
    """
    Validates output header contract against DELIVERY_FORMAT_HEADERS exactly (252 columns),
    then exports deliverable .csv, .xlsx, and separate QA report.
    """
    # 1. HARD HEADER ASSERTION
    output_cols = list(output_df.columns)
    if output_cols != DELIVERY_FORMAT_HEADERS:
        missing = set(DELIVERY_FORMAT_HEADERS) - set(output_cols)
        extra = set(output_cols) - set(DELIVERY_FORMAT_HEADERS)
        err_msg = (
            f"Header contract violated! Expected 252 headers, got {len(output_cols)}. "
            f"Missing: {missing}, Extra: {extra}"
        )
        raise AssertionError(err_msg)

    # 2. Export Deliverable CSV
    output_df.to_csv(csv_path, index=False, encoding="utf-8")
    
    # 3. Export Deliverable XLSX
    output_df.to_excel(xlsx_path, index=False, engine="openpyxl")
    
    # 4. Export QA Sidecar Report
    qa_sidecar_df.to_csv(qa_report_path, index=False, encoding="utf-8")
