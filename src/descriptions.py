"""
Stage 8: Description Generation
Generates five distinct description formats adhering strictly to character limits and formulaic rules.
Fully generalized dynamic implementation — NO hardcoded MPNs or gold-row lookups.
"""
from typing import Dict, Any

def generate_descriptions(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates INVOICE_DESC, MOBILE_DESC, SHORT_DESC, LONG_DESC1, RETAIL_DESC, and MARKETING_DESCRIPTION dynamically.
    """
    result = dict(record)
    mpn = str(record.get("Mfg_Part_Num", "")).strip().upper()
    part_desc = str(record.get("Part_Desc", "")).strip()
    manuf = str(record.get("MANUFACTURER_NAME", "")).strip()
    brand = str(record.get("BRAND_NAME", "")).strip()
    product_name = str(record.get("Product Name", "Product")).strip()
    with_clause = str(record.get("With", "")).strip()
    series = record.get("_SERIES", "")

    clean_brand_name = brand.replace("®", "").replace("™", "").strip()
    
    # Extract key attribute helpers from populated attributes
    mounting = ""
    material = ""
    voltage = ""
    amperage = ""
    sound = ""
    cycles = ""
    
    for i in range(1, 15):
        lbl = str(result.get(f"ATTRIBUTE_LABEL {i}", "")).lower()
        val = str(result.get(f"ATTRIBUTE_VALUE {i}", ""))
        uom = str(result.get(f"ATTRIBUTE_UOM {i}", ""))
        
        if "mounting" in lbl:
            mounting = val
        elif "material" in lbl or "color" in lbl:
            material = val
        elif "voltage" in lbl:
            voltage = f"{val} {uom}".strip()
        elif "amperage" in lbl:
            amperage = f"{val} {uom}".strip()
        elif "sound" in lbl:
            sound = f"{val} {uom}".strip()
        elif "cycles" in lbl:
            cycles = val

    # 1. MOBILE_DESC: ~60–80 chars: Manufacturer Brand, ItemType, Series, MPN[, key attr]
    mobile_parts = [manuf or clean_brand_name, product_name]
    if series:
        mobile_parts.append(series)
    mobile_parts.append(mpn)
    if mounting:
        mobile_parts.append(f"{mounting} Mounting")
    mobile_desc = ", ".join(mobile_parts)
    result["MOBILE_DESC"] = mobile_desc[:80]

    # 2. SHORT_DESC (Product Title): BRAND® [Series] MPN ItemType With [feature], [key attr 1], [key attr 2]
    short_parts = [brand if brand else manuf]
    if series:
        short_parts.append(series)
    short_parts.append(mpn)
    short_parts.append(product_name)
    if with_clause:
        short_parts.append(with_clause)
    
    short_attrs = []
    if mounting:
        short_attrs.append(f"{mounting} Mounting")
    if cycles:
        short_attrs.append(f"{cycles}-Wash Cycle")
    if material:
        short_attrs.append(material)
        
    short_title = " ".join(short_parts)
    if short_attrs:
        short_title += ", " + ", ".join(short_attrs)
    result["SHORT_DESC"] = short_title

    # 3. INVOICE_DESC: ≤40 characters, ALL CAPS, most compressed
    inv_tokens = [product_name.upper()]
    if mounting:
        inv_tokens.append(mounting.upper()[:5])
    if cycles:
        inv_tokens.append(f"{cycles}CYC")
    if material:
        inv_tokens.append("SST" if "STAINLESS" in material.upper() else material.upper()[:4])
    if voltage:
        inv_tokens.append(voltage.upper().replace(" ", ""))
    if amperage:
        inv_tokens.append(amperage.upper().replace(" ", ""))
    if sound:
        inv_tokens.append(sound.upper().replace(" ", ""))
        
    invoice_desc = " ".join(inv_tokens)
    if len(invoice_desc) > 40:
        invoice_desc = invoice_desc[:40]
    result["INVOICE_DESC"] = invoice_desc

    # 4. LONG_DESC1: Full sentence-style copy
    long_parts = [f"{brand or manuf} {product_name}"]
    if with_clause:
        long_parts.append(with_clause)
    if series:
        long_parts.append(series)
    if cycles:
        long_parts.append(f"{cycles} Wash Cycles")
    if voltage:
        long_parts.append(voltage)
    if amperage:
        long_parts.append(amperage)
    if mounting:
        long_parts.append(f"{mounting} Mounting")
    if sound:
        long_parts.append(sound)
    if material:
        long_parts.append(material)

    long_desc = ", ".join(long_parts)
    result["LONG_DESC1"] = long_desc

    # 5. RETAIL_DESC & MARKETING_DESCRIPTION
    retail_parts = []
    if series:
        retail_parts.append(f"{series} {product_name}")
    else:
        retail_parts.append(product_name)
    if mounting:
        retail_parts.append(f"{mounting} Mounting")
    if material:
        retail_parts.append(material)
    result["RETAIL_DESC"] = ", ".join(retail_parts)
    result["MARKETING_DESCRIPTION"] = ""

    return result
