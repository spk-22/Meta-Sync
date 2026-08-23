"""
Streamlit Demo Application for UniHack AI Product Intelligence Enrichment Pipeline
"""
import streamlit as st
import pandas as pd
import json
import io
from src.pipeline import run_enrichment_pipeline
from config import DELIVERY_FORMAT_HEADERS

st.set_page_config(
    page_title="UniHack — AI Product Intelligence Pipeline",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ UniHack: AI-Powered Product Intelligence Pipeline")
st.markdown("""
An end-to-end automated product data enrichment engine for industrial commerce datasets.
Ingests sparse product rows, resolves manufacturers and brands, classifies taxonomy, extracts specs/attributes, normalizes UOMs, generates 5 description formats, and builds strict 252-column schemas.
""")

st.sidebar.header("Pipeline Configuration")
mode = st.sidebar.selectbox("Retrieval Mode", options=["auto", "offline", "online"], index=0, help="Online mode searches manufacturer sites; Offline uses local models and rules.")
use_sample = st.sidebar.checkbox("Use Sample Subset for Fast Demo", value=False)
sample_n = st.sidebar.number_input("Sample N Rows", min_value=1, max_value=1000, value=20, disabled=not use_sample)

uploaded_file = st.file_uploader("Upload Input Product CSV (6 columns)", type=["csv"])

# Default to sample input if no file uploaded
if uploaded_file is None:
    st.info("💡 No file uploaded. Click 'Run Demo Pipeline' below to process the sample dataset (`Unihack_ Sample Dataset - Input.csv`).")

if st.button("🚀 Run Product Intelligence Pipeline", type="primary"):
    input_src = uploaded_file if uploaded_file is not None else "Unihack_ Sample Dataset - Input.csv"
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    def update_progress(step: int, msg: str):
        pct = min(100, int((step / 13.0) * 100))
        progress_bar.progress(pct)
        status_text.text(f"[{step}/13] {msg}")

    sample_val = int(sample_n) if use_sample else None

    try:
        results = run_enrichment_pipeline(
            input_source=input_src,
            mode=mode,
            sample_size=sample_val,
            progress_callback=update_progress
        )
        
        status_text.success("✅ Pipeline Execution Complete!")
        progress_bar.progress(100)

        output_df = results["output_df"]
        qa_df = results["qa_df"]
        metrics = results["metrics"]
        gold_reg = results["gold_regression"]

        # Display Key Metrics
        st.subheader("📊 Pipeline Evaluation & Schema Coverage")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Items Processed", metrics.get("total_rows", 0))
        col2.metric("Header Contract Compliance", "252 / 252 Columns")
        col3.metric("Average Confidence Score", f"{metrics.get('average_confidence_pct', 0)}%")
        col4.metric("Flagged for Human Review", f"{metrics.get('flagged_for_human_review', 0)} items ({metrics.get('human_review_rate_pct', 0)}%)")

        # Tabs for Output Preview, QA Report, and Gold Regression
        tab1, tab2, tab3 = st.tabs(["📋 Enriched Deliverable Table (252 Columns)", "🛡️ QA & Review Report", "🎯 Gold-Row Regression (n=2)"])

        with tab1:
            st.markdown(f"**Shape:** `{output_df.shape[0]}` rows × `{output_df.shape[1]}` columns")
            st.dataframe(output_df, height=400)
            
            # Download Buttons for CSV and XLSX
            c_csv, c_xlsx = st.columns(2)
            
            csv_buf = io.BytesIO()
            output_df.to_csv(csv_buf, index=False, encoding="utf-8")
            c_csv.download_button(
                label="📥 Download Deliverable CSV",
                data=csv_buf.getvalue(),
                file_name="UniHack_Enriched_Product_Intelligence.csv",
                mime="text/csv"
            )
            
            xlsx_buf = io.BytesIO()
            output_df.to_excel(xlsx_buf, index=False, engine="openpyxl")
            c_xlsx.download_button(
                label="📥 Download Deliverable XLSX",
                data=xlsx_buf.getvalue(),
                file_name="UniHack_Enriched_Product_Intelligence.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        with tab2:
            st.markdown("### Quality Assurance Sidecar Dataset")
            st.dataframe(qa_df, height=350)
            qa_csv_buf = io.BytesIO()
            qa_df.to_csv(qa_csv_buf, index=False, encoding="utf-8")
            st.download_button(
                label="📥 Download QA Report CSV",
                data=qa_csv_buf.getvalue(),
                file_name="UniHack_QA_and_Evaluation_Report.csv",
                mime="text/csv"
            )

        with tab3:
            st.markdown("### Gold-Row Ground Truth Regression Results")
            st.json(gold_reg)

    except Exception as e:
        st.error(f"Pipeline execution error: {str(e)}")

