"""
Stage 12: Evaluation Harness
Gold-row field-by-field regression diff against Expected Output CSV (n=2),
plus schema-compliance and coverage metrics across full batch runs.
"""
import pandas as pd
from typing import Dict, Any, List, Tuple
from config import DELIVERY_FORMAT_HEADERS

def run_gold_row_regression(pipeline_output_df: pd.DataFrame, expected_output_csv_path: str = "Unihack_ Expected Output - Delivery Format.csv") -> Dict[str, Any]:
    """
    Evaluates pipeline output against the ground truth gold rows in expected_output_csv_path.
    Diffs all 252 fields.
    """
    expected_df = pd.read_csv(expected_output_csv_path, dtype=str).fillna("")
    
    regression_results = {}
    
    for _, exp_row in expected_df.iterrows():
        mpn = str(exp_row.get("Mfg_Part_Num", "")).strip()
        if not mpn:
            continue
            
        pred_match = pipeline_output_df[pipeline_output_df["Mfg_Part_Num"] == mpn]
        if pred_match.empty:
            regression_results[mpn] = {
                "found": False,
                "exact_matches": 0,
                "total_fields": 252,
                "field_diffs": {},
                "match_rate": 0.0
            }
            continue
            
        pred_row = pred_match.iloc[0]
        exact_matches = 0
        field_diffs = {}
        
        for col in DELIVERY_FORMAT_HEADERS:
            exp_val = str(exp_row.get(col, "")).strip()
            pred_val = str(pred_row.get(col, "")).strip()
            
            # Case insensitive & symbol-normalized comparison for equality check
            exp_norm = exp_val.replace("®", "").replace("™", "").lower()
            pred_norm = pred_val.replace("®", "").replace("™", "").lower()
            
            if exp_norm == pred_norm:
                exact = True
            else:
                exact = False
                
            if exact:
                exact_matches += 1
            else:
                field_diffs[col] = {
                    "expected": exp_val,
                    "predicted": pred_val
                }
                
        match_rate = exact_matches / 252.0
        regression_results[mpn] = {
            "found": True,
            "exact_matches": exact_matches,
            "total_fields": 252,
            "field_diffs": field_diffs,
            "match_rate": round(match_rate * 100.0, 2)
        }
        
    return regression_results

def compute_dataset_metrics(pipeline_output_df: pd.DataFrame, qa_sidecar_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes schema compliance, coverage, and review metrics across full dataset.
    """
    total_rows = len(pipeline_output_df)
    if total_rows == 0:
        return {}

    def non_blank_rate(col: str) -> float:
        if col not in pipeline_output_df.columns:
            return 0.0
        non_blanks = (pipeline_output_df[col].astype(str).str.strip() != "").sum()
        return round((non_blanks / total_rows) * 100.0, 2)

    # Invoice desc char limit compliance
    inv_col = pipeline_output_df.get("INVOICE_DESC", pd.Series([""] * total_rows))
    inv_compliant = (inv_col.astype(str).str.len() <= 40).sum()
    inv_compliance_rate = round((inv_compliant / total_rows) * 100.0, 2)

    # Calculate average attributes per row
    attr_label_cols = [f"ATTRIBUTE_LABEL {i}" for i in range(1, 51)]
    attr_counts = 0
    for col in attr_label_cols:
        if col in pipeline_output_df.columns:
            attr_counts += (pipeline_output_df[col].astype(str).str.strip() != "").sum()
    avg_attrs = round(attr_counts / total_rows, 2)

    needs_review_count = 0
    avg_confidence = 100.0
    if "needs_human_review" in qa_sidecar_df.columns:
        needs_review_count = qa_sidecar_df["needs_human_review"].astype(bool).sum()
    if "confidence_score" in qa_sidecar_df.columns:
        avg_confidence = round(qa_sidecar_df["confidence_score"].mean() * 100.0, 2)

    needs_review_count = int(needs_review_count)
    total_rows = int(total_rows)
    avg_attributes = float(avg_attrs)
    avg_conf = float(avg_confidence)

    metrics = {
        "total_rows": total_rows,
        "non_blank_rates": {
            "MANUFACTURER_NAME": float(non_blank_rate("MANUFACTURER_NAME")),
            "BRAND_NAME": float(non_blank_rate("BRAND_NAME")),
            "Classpath": float(non_blank_rate("Classpath")),
            "INVOICE_DESC": float(non_blank_rate("INVOICE_DESC")),
            "MOBILE_DESC": float(non_blank_rate("MOBILE_DESC")),
            "SHORT_DESC": float(non_blank_rate("SHORT_DESC")),
            "LONG_DESC1": float(non_blank_rate("LONG_DESC1")),
            "Product Image": float(non_blank_rate("Product Image")),
        },
        "invoice_desc_char_compliance_pct": float(inv_compliance_rate),
        "avg_attributes_per_item": avg_attributes,
        "average_confidence_pct": avg_conf,
        "flagged_for_human_review": needs_review_count,
        "human_review_rate_pct": round((needs_review_count / total_rows) * 100.0, 2)
    }
    return metrics
