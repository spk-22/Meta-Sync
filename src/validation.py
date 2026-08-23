"""
Stage 11: Validation and Confidence Scoring
Calculates per-row confidence scores and sets needs_human_review flags for the QA sidecar report.
"""
from typing import Dict, Any, Tuple

def validate_and_score_row(assembled_row: Dict[str, str], groundedness: float = 1.0) -> Tuple[float, bool, str]:
    """
    Computes confidence score (0.0 to 1.0), needs_human_review (bool), and review_reason (str).
    Sidecar only — NOT included in the 252 delivery headers.
    """
    reasons = []
    score_components = []

    mpn = assembled_row.get("Mfg_Part_Num", "")
    manuf = assembled_row.get("MANUFACTURER_NAME", "")
    brand = assembled_row.get("BRAND_NAME", "")
    classpath = assembled_row.get("Classpath", "")
    invoice_desc = assembled_row.get("INVOICE_DESC", "")
    short_desc = assembled_row.get("SHORT_DESC", "")

    # 1. Manufacturer/Brand resolution score
    if manuf and brand:
        score_components.append(1.0)
    elif manuf or brand:
        score_components.append(0.7)
    else:
        score_components.append(0.0)
        reasons.append("Missing Manufacturer/Brand")

    # 2. Taxonomy score
    if classpath:
        score_components.append(1.0)
    else:
        score_components.append(0.5)
        reasons.append("Missing Classpath")

    # 3. Description char limit compliance score
    desc_score = 1.0
    if len(invoice_desc) > 40:
        desc_score -= 0.3
        reasons.append(f"INVOICE_DESC exceeds 40 chars ({len(invoice_desc)})")
    if not short_desc:
        desc_score -= 0.3
        reasons.append("Missing SHORT_DESC")
    score_components.append(max(0.0, desc_score))

    # 4. Attribute groundedness score
    score_components.append(groundedness)

    # Calculate overall weighted confidence score
    confidence_score = sum(score_components) / len(score_components)
    
    needs_review = confidence_score < 0.8 or len(reasons) > 0
    reason_str = "; ".join(reasons) if reasons else "Clean"

    return round(confidence_score, 4), needs_review, reason_str
