# SecureScore — Alternative Credit Scoring & DPDP Compliance Layer

## Project Overview
SecureScore is a fintech-oriented Proof-of-Concept (POC) designed to assess the creditworthiness of unbanked and thin-file users in India using alternative behavioral data (UPI transactions, bill payments, and app activity). 

Crucially, it incorporates a comprehensive security and auditing layer compliant with India's Digital Personal Data Protection (DPDP) Act.

## Key Features
- **Behavioral Scoring**: Uses Faker synthetic data (50k users) and an XGBoost model to predict default probability.
- **Credit Score Scale**: Maps probabilities to a 300–900 standard credit score scale.
- **Explainable AI (XAI)**: Employs SHAP (SHapley Additive exPlanations) for per-user explainability of scores.
- **Data Protection (AES-256)**: Performs field-level encryption for sensitive PII (User ID, State, Income estimates).
- **Access Pattern Monitoring**: Real-time rule-based anomaly detection to prevent credential sharing and bulk data exports.
- **Compliance Auditing**: A built-in 8-rule compliance engine producing automated compliance audits (`dpdp_report.json`).
- **Interactive Dashboard**: A 4-screen Streamlit application to query scores, inspect explanations, monitor security events, and view DPDP audits.

## Directory Structure
```
securescore/
├── data/
│   ├── generate_data.py          # Synthetic dataset generator
│   └── users_raw.csv             # Raw generated dataset (ignored)
├── pipeline/
│   └── etl.py                    # ETL pipeline to SQLite
├── model/
│   ├── features.py               # Feature engineering module
│   ├── train.py                  # XGBoost model training
│   ├── score.py                  # Credit score calculation
│   └── explain.py                # SHAP explanation generation
├── security/
│   ├── encrypt.py                # AES-256 field encryption/decryption
│   ├── anomaly.py                # Access pattern anomaly monitoring
│   └── dpdp_audit.py             # 8-rule DPDP audit engine
├── dashboard/
│   └── app.py                    # Streamlit Dashboard application
├── models/
│   └── .gitkeep                  # XGBoost and Scaler model binaries directory (ignored)
├── reports/
│   └── .gitkeep                  # Model validation outputs and audit results (ignored)
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Docker (optional)

### Local Environment Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - **Windows (PowerShell)**: `.venv\Scripts\Activate.ps1`
   - **macOS/Linux**: `source .venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
