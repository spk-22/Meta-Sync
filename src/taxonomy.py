"""
Stage 4: Classification and Taxonomy
Maps Part_Desc and resolved Manufacturer/Brand to Dept, Class, Fine, and Classpath.
"""
from typing import Dict, Any
from config import TAXONOMY_RULES

def classify_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classifies a record into Dept, Class, Fine, Classpath using keyword rules and heuristics.
    """
    desc = str(record.get("Part_Desc", "")).lower()
    manuf = str(record.get("MANUFACTURER_NAME", "")).lower()
    brand = str(record.get("BRAND_NAME", "")).lower()
    combined_text = f"{desc} {manuf} {brand}"
    
    matched_dept = ""
    matched_class = ""
    matched_fine = ""
    matched_classpath = ""
    
    for rule in TAXONOMY_RULES:
        if any(kw in combined_text for kw in rule["keywords"]):
            matched_dept = rule["dept"]
            matched_class = rule["class"]
            matched_fine = rule["fine"]
            matched_classpath = rule["classpath"]
            break
            
    # Default fallback classification if no keyword rule matched
    if not matched_dept:
        matched_dept = "Tools & Industrial Hardware"
        matched_class = "Industrial Maintenance"
        matched_fine = "General Supplies"
        matched_classpath = "Tools & Industrial Hardware>Industrial Maintenance>General Supplies"
        
    result = dict(record)
    result["Dept"] = matched_dept
    result["Class"] = matched_class
    result["Fine"] = matched_fine
    result["Classpath"] = matched_classpath
    return result
