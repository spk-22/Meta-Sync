"""
Stage 1: Placeholder Cleaning
Filters out placeholder brand strings like '-- Unbranded --', '-- No Unilog Brand --', etc.
Preserves raw input fields for verbatim passthrough in output, while populating _clean_* fields for pipeline matching logic.
"""
from typing import Dict, Any, Optional
from config import PLACEHOLDER_STRINGS

def clean_placeholder(val: Optional[str]) -> Optional[str]:
    """
    Returns None if val matches any placeholder string, else returns trimmed string.
    """
    if val is None:
        return None
    cleaned = str(val).strip()
    if cleaned.lower() in PLACEHOLDER_STRINGS:
        return None
    return cleaned

def clean_record_placeholders(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Preserves raw input fields in record and stores cleaned values in internal '_clean_*' fields.
    """
    cleaned_record = dict(record)
    
    for key in ["E1_Brand", "Unilog_Brand", "DIB_Brand", "Part_Manuf", "Part_Desc", "Mfg_Part_Num"]:
        raw_val = cleaned_record.get(key, "")
        c_val = clean_placeholder(raw_val)
        cleaned_record[f"_clean_{key}"] = c_val if c_val is not None else ""
        
    return cleaned_record
