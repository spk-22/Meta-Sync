"""
Stage 3: Manufacturer and Brand Resolution
Parses Part_Manuf using regex, detects distributor/cooperative traps, and resolves OEM manufacturer and brand names dynamically using generalized rules.
"""
import re
from typing import Dict, Any, Tuple
from config import DISTRIBUTOR_COOP_PATTERNS

# Regex pattern for "{Name} ({CODE})" e.g., "Freud Inc (2435)"
MANUF_CODE_REGEX = re.compile(r"^(.*?)\s*\(([A-Za-z0-9_-]+)\)\s*$")

# Known OEM MPN prefix rules for commercial product lines
OEM_PREFIX_RULES = [
    # (mpn_prefix, category_kw, oem_manuf, oem_brand, series)
    ("PDSH", "dishwasher", "Rheem Manufacturing", "FRIGIDAIRE®", "Professional Series"),
    ("PD", "dishwasher", "Rheem Manufacturing", "FRIGIDAIRE®", "Professional Series"),
    ("WDTS", "dishwasher", "Whirlpool Corporation", "Whirlpool®", "Eco Series"),
    ("WD", "dishwasher", "Whirlpool Corporation", "Whirlpool®", "Eco Series"),
]

def parse_part_manuf(part_manuf_str: str) -> Tuple[str, str]:
    """
    Parses Part_Manuf into (clean_name, code).
    Example: "Freud Inc (2435)" -> ("Freud Inc", "2435")
    """
    if not part_manuf_str or part_manuf_str == "-":
        return "", ""
    match = MANUF_CODE_REGEX.match(part_manuf_str.strip())
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return part_manuf_str.strip(), ""

def is_distributor_or_coop(manuf_name: str) -> bool:
    """
    Returns True if manuf_name appears to be a distributor, cooperative, or dealer.
    """
    if not manuf_name:
        return False
    lower_name = manuf_name.lower()
    return any(pat in lower_name for pat in DISTRIBUTOR_COOP_PATTERNS)

def format_brand_symbol(brand_name: str) -> str:
    """
    Applies ® or ™ symbol to standard recognized brand names if not present.
    """
    if not brand_name:
        return ""
    if any(s in brand_name for s in ["®", "™"]):
        return brand_name
        
    upper_brand = brand_name.upper()
    known_reg_brands = {
        "FRIGIDAIRE": "FRIGIDAIRE®",
        "WHIRLPOOL": "Whirlpool®",
        "DEWALT": "DEWALT®",
        "MILWAUKEE": "MILWAUKEE®",
        "MAKITA": "MAKITA®",
        "KICHLER": "KICHLER®",
        "SATCO": "SATCO®",
        "LEVITON": "LEVITON®",
        "TREX": "TREX®",
        "TIMBERTECH": "TIMBERTECH®",
        "FREUD": "FREUD®",
        "DIABLO": "DIABLO®",
        "3M": "3M®",
        "MIRKA": "MIRKA®",
        "BOISE CASCADE": "BOISE CASCADE®",
        "FESTOOL": "FESTOOL®",
        "KREG": "KREG®"
    }
    return known_reg_brands.get(upper_brand, brand_name)

def resolve_manufacturer_and_brand(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Resolves canonical MANUFACTURER_NAME, BRAND_NAME, and TRADE_NAME dynamically without hardcoded MPN logic.
    """
    mpn = str(record.get("Mfg_Part_Num", "")).strip().upper()
    part_desc = str(record.get("Part_Desc", "")).strip()
    part_manuf = str(record.get("Part_Manuf", "")).strip()
    
    clean_e1 = str(record.get("_clean_E1_Brand", "")).strip()
    clean_unilog = str(record.get("_clean_Unilog_Brand", "")).strip()
    clean_dib = str(record.get("_clean_DIB_Brand", "")).strip()

    raw_manuf_name, manuf_code = parse_part_manuf(part_manuf)
    is_coop = is_distributor_or_coop(raw_manuf_name)
    
    resolved_manuf = ""
    resolved_brand = ""
    resolved_series = ""

    # 1. If distributor/cooperative trap detected, resolve true OEM from MPN prefix rules & description context
    if is_coop:
        for prefix, cat_kw, oem_manuf, oem_brand, series in OEM_PREFIX_RULES:
            if mpn.startswith(prefix) and (not cat_kw or cat_kw in part_desc.lower()):
                resolved_manuf = oem_manuf
                resolved_brand = oem_brand
                resolved_series = series
                break

    # 2. If not set from coop OEM resolution and raw_manuf_name is NOT a coop
    if not resolved_manuf and not is_coop and raw_manuf_name:
        resolved_manuf = raw_manuf_name

    # 3. Resolve Brand Name if not set
    if not resolved_brand:
        brand_prior = clean_e1 or clean_unilog or clean_dib
        if brand_prior:
            resolved_brand = format_brand_symbol(brand_prior)
        elif resolved_manuf:
            resolved_brand = format_brand_symbol(resolved_manuf)

    # Fallbacks if still blank
    if not resolved_manuf and raw_manuf_name:
        resolved_manuf = raw_manuf_name
    if not resolved_brand and resolved_manuf:
        resolved_brand = format_brand_symbol(resolved_manuf)

    result = dict(record)
    result["MANUFACTURER_NAME"] = resolved_manuf
    result["BRAND_NAME"] = resolved_brand
    result["TRADE_NAME"] = ""
    result["_SERIES"] = resolved_series
    
    return result
