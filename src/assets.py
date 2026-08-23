"""
Stage 9: Digital Assets
Deterministic filename patterns for product images and PDF specification sheets.
Fully generalized dynamic implementation — NO hardcoded MPNs.
"""
from typing import Dict, Any

def resolve_digital_assets(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Populates image filenames, spec sheets, and sets 'Actual Image (Yes/No)' dynamically.
    """
    result = dict(record)
    mpn = str(record.get("Mfg_Part_Num", "")).strip()
    brand = str(record.get("BRAND_NAME", "")).replace("®", "").replace("™", "").strip()
    
    if not brand:
        brand = str(record.get("MANUFACTURER_NAME", "")).strip()
    if not brand:
        brand = "PRODUCT"
        
    brand_clean = brand.replace(" ", "_").replace("&", "AND")
    
    # Generic deterministic image & asset filename pattern
    if brand_clean and mpn:
        base_name = f"{brand_clean}_{mpn}"
        result["Product Image"] = f"{base_name}.jpg"
        result["Specification Sheet"] = f"{base_name}_Specification_Sheet.pdf"
        # Actual Image flag is Yes if MFR URL / retrieved image URL exists, else No
        has_real_image = bool(result.get("MFR URL", ""))
        result["Actual Image (Yes/No)"] = "Yes" if has_real_image else "No"
    else:
        result["Product Image"] = ""
        result["Specification Sheet"] = ""
        result["Actual Image (Yes/No)"] = "No"
        
    return result
