"""
Stage 0: Ingest & Profile
Loads input CSV, validates required 6 columns, cleans raw strings.
"""
import pandas as pd
from typing import List, Dict, Any, Tuple

REQUIRED_INPUT_COLUMNS = [
    "Mfg_Part_Num", "Part_Desc", "E1_Brand", "Unilog_Brand", "DIB_Brand", "Part_Manuf"
]

def load_and_validate_input(file_path_or_buffer) -> pd.DataFrame:
    """
    Loads CSV from path or file buffer, validates the 6 required columns exist.
    """
    df = pd.read_csv(file_path_or_buffer, dtype=str)
    # Strip whitespace from column names
    df.columns = [str(c).strip() for c in df.columns]
    
    missing = [col for col in REQUIRED_INPUT_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Input dataset is missing required columns: {missing}. Found columns: {list(df.columns)}")
    
    # Fill NaN values with empty string
    df = df.fillna("")
    
    # Trim leading/trailing whitespace in string cells
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        
    return df
