"""
Stage 2: De-duplication & Alternate Part Number Resolution
Fuzzy-matches MPN and manufacturer names to group near-duplicates and populate ALTERNATE_PART_NUMBER.
"""
from typing import List, Dict, Any
from rapidfuzz import fuzz
from src.resolution import parse_part_manuf

def process_deduplication(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Scans records to find equivalent/alternate MPNs and populates ALTERNATE_PART_NUMBER.
    """
    processed = [dict(r) for r in records]
    n = len(processed)
    
    # Map index to alternate MPNs found
    alternates_map = {i: set() for i in range(n)}
    
    for i in range(n):
        mpn_i = str(processed[i].get("Mfg_Part_Num", "")).strip().upper()
        manuf_i, _ = parse_part_manuf(str(processed[i].get("Part_Manuf", "")))
        if not mpn_i:
            continue
            
        for j in range(i + 1, n):
            mpn_j = str(processed[j].get("Mfg_Part_Num", "")).strip().upper()
            manuf_j, _ = parse_part_manuf(str(processed[j].get("Part_Manuf", "")))
            if not mpn_j or mpn_i == mpn_j:
                continue
                
            # If MPN is substring or fuzzy ratio > 90 and manufacturer matches
            if manuf_i and manuf_j and manuf_i.lower() == manuf_j.lower():
                ratio = fuzz.ratio(mpn_i, mpn_j)
                if ratio >= 90:
                    alternates_map[i].add(mpn_j)
                    alternates_map[j].add(mpn_i)
                    
    for i in range(n):
        mpn = str(processed[i].get("Mfg_Part_Num", "")).strip()
        alts = sorted(list(alternates_map[i]))
        processed[i]["MANUFACTURER_PART_NUMBER"] = mpn
        processed[i]["ALTERNATE_PART_NUMBER"] = ", ".join(alts) if alts else ""
        
    return processed
