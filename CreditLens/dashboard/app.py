"""
Streamlit dashboard application for SecureScore.
Contains 4 screens:
- Screen 1: Credit Score (Gauge & Explanations)
- Screen 2: Explainability (SHAP details)
- Screen 3: Security Monitor (Anomalies & Stats)
- Screen 4: DPDP Audit (Rules checklist)
"""

import streamlit as st

def main():
    st.set_page_config(page_title="SecureScore Dashboard", layout="wide")
    st.title("SecureScore - Credit Scoring & DPDP Compliance Dashboard")
    
if __name__ == "__main__":
    main()
