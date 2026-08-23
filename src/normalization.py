"""
Stage 7: Normalization
UOM standardization, decimal to mixed-fraction conversion, title casing, and spacing rules.
"""
import math
from typing import Dict, Any, Union
from config import STANDARD_UOM_MAP

def gcd(a: int, b: int) -> int:
    return math.gcd(a, b)

def decimal_to_fraction(val: float) -> str:
    """
    Converts a decimal number to a mixed fraction string rounded to the nearest 1/64.
    Examples:
    50.25 -> "50-1/4"
    33.4375 -> "33-7/16"
    50.1875 -> "50-3/16"
    0.5 -> "1/2"
    50.0 -> "50"
    """
    if val is None or math.isnan(val):
        return ""
        
    negative = val < 0
    val = abs(val)
    
    integer_part = int(math.floor(val))
    remainder = val - integer_part
    
    if remainder < 1e-5:
        res = str(integer_part)
        return f"-{res}" if negative else res
        
    num_64 = int(round(remainder * 64))
    if num_64 == 0:
        res = str(integer_part)
        return f"-{res}" if negative else res
    elif num_64 == 64:
        res = str(integer_part + 1)
        return f"-{res}" if negative else res
        
    common = gcd(num_64, 64)
    num = num_64 // common
    den = 64 // common
    
    frac_str = f"{num}/{den}"
    if integer_part == 0:
        res = frac_str
    else:
        res = f"{integer_part}-{frac_str}"
        
    return f"-{res}" if negative else res

def normalize_uom(uom_str: str) -> str:
    """
    Normalizes unit of measure using standard dictionary.
    """
    if not uom_str:
        return ""
    clean = str(uom_str).strip().lower()
    return STANDARD_UOM_MAP.get(clean, str(uom_str).strip())

def format_value_with_uom(val: str, uom: str) -> str:
    """
    Ensures a single space between number and unit (e.g. '24 in', never '24in').
    """
    if not val:
        return ""
    norm_uom = normalize_uom(uom)
    if not norm_uom:
        return val.strip()
    return f"{val.strip()} {norm_uom}"

def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Applies Stage 7 normalization across all attributes and fields in a record.
    """
    result = dict(record)
    
    # Normalize Attribute UOMs and Values
    for i in range(1, 51):
        uom_key = f"ATTRIBUTE_UOM {i}"
        val_key = f"ATTRIBUTE_VALUE {i}"
        label_key = f"ATTRIBUTE_LABEL {i}"
        
        if uom_key in result and result[uom_key]:
            result[uom_key] = normalize_uom(result[uom_key])
            
        if label_key in result and result[label_key]:
            # Title Case attribute labels if not Special
            label_val = str(result[label_key]).strip()
            if label_val not in ["UPC", "EAN", "GTIN", "UNSPSC", "SDS", "MTR", "RoHS"]:
                # Keep words in Title Case
                result[label_key] = label_val.title() if not label_val.istitle() else label_val

    return result
