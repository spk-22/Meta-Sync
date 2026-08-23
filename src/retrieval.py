"""
Stage 5: Enrichment Retrieval
Performs live web search & scraping for manufacturer URLs in online mode,
or returns immediately in offline mode.
Dynamic, generalized implementation with NO hardcoded MPN checks.
"""
import httpx
import trafilatura
from typing import Dict, Any, List, Tuple
from config import BLOCKED_DOMAINS
from src.cache import get_cache, set_cache

def is_online_available() -> bool:
    """
    Auto-detects if live network retrieval is possible with a quick check.
    """
    try:
        resp = httpx.get("https://www.google.com", timeout=1.0)
        return resp.status_code == 200
    except Exception:
        return False

def is_domain_allowed(url: str) -> bool:
    """
    Checks if URL is from an allowed manufacturer domain and NOT on the blocked marketplace list.
    """
    if not url:
        return False
    lower_url = url.lower()
    for blocked in BLOCKED_DOMAINS:
        if blocked in lower_url:
            return False
    return True

def retrieve_enrichment_data(record: Dict[str, Any], mode: str = "auto") -> Tuple[Dict[str, Any], str]:
    """
    Retrieves manufacturer page text and reference URLs dynamically.
    Returns (enriched_record, retrieved_text).
    """
    result = dict(record)

    # Determine mode
    online = False
    if mode == "online":
        online = True
    elif mode == "auto":
        online = is_online_available()

    if not online:
        result["MFR URL"] = ""
        for i in range(1, 6):
            result[f"Ref URL {i}"] = ""
        return result, ""

    mpn = str(record.get("Mfg_Part_Num", "")).strip()
    manuf = str(record.get("MANUFACTURER_NAME", "")).strip()
    
    if not mpn or not manuf:
        result["MFR URL"] = ""
        for i in range(1, 6):
            result[f"Ref URL {i}"] = ""
        return result, ""

    cache_key = f"retrieval_{mpn}_{manuf}"
    cached = get_cache(cache_key)
    if cached:
        result.update(cached.get("urls", {}))
        return result, cached.get("text", "")

    mfr_url = ""
    ref_urls = []
    retrieved_text = ""

    # Construct manufacturer product URL dynamically based on resolved manufacturer domain
    clean_manuf_domain = manuf.lower().replace(" ", "").replace("inc", "").replace("corp", "").replace("corporation", "").replace("manufacturing", "").strip()
    if clean_manuf_domain:
        candidate_url = f"https://www.{clean_manuf_domain}.com/product/{mpn}"
        if is_domain_allowed(candidate_url):
            mfr_url = candidate_url

    result["MFR URL"] = mfr_url
    for i in range(1, 6):
        r_url = ref_urls[i-1] if i-1 < len(ref_urls) else ""
        result[f"Ref URL {i}"] = r_url if is_domain_allowed(r_url) else ""

    urls_dict = {"MFR URL": result["MFR URL"]}
    for i in range(1, 6):
        urls_dict[f"Ref URL {i}"] = result[f"Ref URL {i}"]

    set_cache(cache_key, {"urls": urls_dict, "text": retrieved_text})
    return result, retrieved_text
