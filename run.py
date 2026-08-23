"""
CLI entry point for running the UniHack AI Product Intelligence Enrichment Pipeline.
"""
import argparse
import sys
import os
import json
from src.pipeline import run_enrichment_pipeline
from src.resolution import resolve_manufacturer_and_brand

def main():
    parser = argparse.ArgumentParser(description="UniHack AI Product Intelligence Enrichment Pipeline CLI")
    parser.add_argument("--input", type=str, default="Unihack_ Sample Dataset - Input.csv", help="Input CSV file path")
    parser.add_argument("--mode", type=str, choices=["online", "offline", "auto"], default="offline", help="Retrieval mode (default: offline)")
    parser.add_argument("--sample", type=int, default=None, help="Sample size limit for fast iteration")
    parser.add_argument("--output-csv", type=str, default="UniHack_Enriched_Product_Intelligence.csv", help="Deliverable CSV output path")
    parser.add_argument("--output-xlsx", type=str, default="UniHack_Enriched_Product_Intelligence.xlsx", help="Deliverable XLSX output path")
    parser.add_argument("--qa-report", type=str, default="UniHack_QA_and_Evaluation_Report.csv", help="QA report sidecar CSV output path")
    parser.add_argument("--run-gold-test", action="store_true", help="Run Stage 3 Gold-row regression check explicitly")

    args = parser.parse_args()

    if args.run_gold_test:
        print("=== STAGE 3 GOLD-ROW REGRESSION TEST ===")
        gold1 = {"Mfg_Part_Num": "PDSH4816AF", "Part_Desc": "PDSH4816AF Dishwasher SS", "Part_Manuf": "Appliance Dealers Cooperative (APPDE)"}
        gold2 = {"Mfg_Part_Num": "WDTS7024RZ", "Part_Desc": "WDTS7024RZ Dishwasher SS", "Part_Manuf": "Appliance Dealers Cooperative (APPDE)"}
        
        r1 = resolve_manufacturer_and_brand(gold1)
        r2 = resolve_manufacturer_and_brand(gold2)

        print("Gold Row 1 (PDSH4816AF):")
        print(f"  Manufacturer: {r1['MANUFACTURER_NAME']} (Expected: Rheem Manufacturing)")
        print(f"  Brand: {r1['BRAND_NAME']} (Expected: FRIGIDAIRE®)")

        print("Gold Row 2 (WDTS7024RZ):")
        print(f"  Manufacturer: {r2['MANUFACTURER_NAME']} (Expected: Whirlpool Corporation)")
        print(f"  Brand: {r2['BRAND_NAME']} (Expected: Whirlpool®)")

        assert r1['MANUFACTURER_NAME'] == "Rheem Manufacturing", "Stage 3 Gold Test 1 Failed for Manufacturer!"
        assert r1['BRAND_NAME'] == "FRIGIDAIRE®", "Stage 3 Gold Test 1 Failed for Brand!"
        assert r2['MANUFACTURER_NAME'] == "Whirlpool Corporation", "Stage 3 Gold Test 2 Failed for Manufacturer!"
        assert r2['BRAND_NAME'] == "Whirlpool®", "Stage 3 Gold Test 2 Failed for Brand!"
        print("[SUCCESS] STAGE 3 GOLD-ROW REGRESSION TEST PASSED PERFECTLY!\n")

    print(f"Running pipeline on '{args.input}' in mode '{args.mode}'...")
    if args.sample:
        print(f"Sample size: first {args.sample} rows")

    def print_progress(stage_num: int, msg: str):
        print(f"[{stage_num}/13] {msg}")

    results = run_enrichment_pipeline(
        input_source=args.input,
        mode=args.mode,
        sample_size=args.sample,
        progress_callback=print_progress,
        export_csv=args.output_csv,
        export_xlsx=args.output_xlsx,
        export_qa=args.qa_report
    )

    print("\n" + "="*50)
    print("PIPELINE SUMMARY & EVALUATION REPORT")
    print("="*50)
    print(json.dumps(results["metrics"], indent=2))
    
    print("\nGOLD-ROW REGRESSION RESULTS (n=2):")
    print(json.dumps(results["gold_regression"], indent=2))

    print(f"\nFiles exported:")
    print(f"  - Deliverable CSV:  {args.output_csv}")
    print(f"  - Deliverable XLSX: {args.output_xlsx}")
    print(f"  - QA Report:        {args.qa_report}")

if __name__ == "__main__":
    main()
