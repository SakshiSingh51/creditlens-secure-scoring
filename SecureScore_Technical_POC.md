# SecureScore — Technical POC Document
### Alternative Credit Scoring + Cybersecurity Layer | Fintech Portfolio Project

---

## 1. PROBLEM STATEMENT

**Core Problem:**
India has 500M people with zero credit history. Traditional CIBIL-based scoring excludes them entirely. Fintech lenders have no way to assess their creditworthiness.

**Secondary Problem (2026 specific):**
India's DPDP Act (effective June 2026) mandates that any personal financial data used for credit decisions must be encrypted, consent-driven, and auditable. Most alternative scoring systems being built today have NO security layer — making them non-compliant by default.

**What SecureScore Solves:**
- Scores unbanked users using behavioral alternative data (UPI, bills, app usage)
- Does it with AES-256 encryption, anomaly detection, and DPDP audit built-in
- Every score is explainable — no black box

---

## 2. TARGETED COMPANIES

| Company | Why This Project Hits Them Directly |
|---|---|
| **Slice / KreditBee** | Alternative credit IS their core product |
| **BharatPe** | MSME credit scoring for unbanked merchants |
| **CRED** | Obsessed with data security and trust |
| **Razorpay** | Payments + fraud + compliance is their world |
| **PhonePe** | UPI behavioral data is their biggest asset |
| **Groww** | Financial inclusion + data privacy priority |
| **Navi / Kissht** | Digital lending to thin-file customers |

---

## 3. TECH STACK

| Layer | Tool | Purpose |
|---|---|---|
| Language | Python 3.10 | Core |
| Data Generation | Faker | Synthetic dataset (50K users) |
| Data Processing | Pandas, NumPy | Cleaning, feature engineering |
| ML Model | XGBoost | Credit scoring model |
| Explainability | SHAP | Per-user score explanation |
| Encryption | Python cryptography (AES-256) | PII protection |
| Anomaly Detection | Rule-based Python | Access pattern monitoring |
| Compliance | Custom Python audit module | DPDP Act 8-rule checker |
| Dashboard | Streamlit | Live interactive POC |
| Hosting | Streamlit Cloud | Free public URL for recruiters |
| Database | SQLite (POC) | Zero setup, file-based |
| Version Control | GitHub | Portfolio visibility |

**No paid services. No cloud costs. Total cost = ₹0**

---

## 4. FILE STRUCTURE

```
securescore/
│
├── data/
│   ├── generate_data.py          # Synthetic dataset generator (Faker)
│   └── users_raw.csv             # Generated: 50K synthetic users
│
├── pipeline/
│   └── etl.py                    # Ingest → Clean → Validate → Load to SQLite
│
├── model/
│   ├── features.py               # Feature engineering
│   ├── train.py                  # XGBoost training + save model
│   ├── score.py                  # Score a single user (300–900 scale)
│   └── explain.py                # SHAP explanation per user
│
├── security/
│   ├── encrypt.py                # AES-256 encrypt/decrypt PII fields
│   ├── anomaly.py                # Flag suspicious access patterns
│   └── dpdp_audit.py             # 8-rule DPDP compliance checker
│
├── dashboard/
│   └── app.py                    # Streamlit app (4 screens)
│
├── models/
│   ├── securescore_model.pkl     # Saved XGBoost model
│   └── scaler.pkl                # Saved feature scaler
│
├── reports/
│   ├── model_performance.png     # ROC curve + confusion matrix
│   ├── shap_summary.png          # Feature importance plot
│   └── dpdp_report.json          # Compliance audit output
│
├── requirements.txt
├── .gitignore                    # Excludes *.key, *.pkl, .env
└── README.md
```

---

## 5. HLD — HIGH LEVEL DESIGN

```
┌──────────────────────────────────────────────────────────────┐
│                      SECURESCORE POC                          │
│                                                               │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│   │  DATA       │     │  SCORING    │     │  SECURITY   │   │
│   │  LAYER      │────▶│  ENGINE     │────▶│  LAYER      │   │
│   │             │     │             │     │             │   │
│   │ Faker data  │     │ XGBoost     │     │ AES-256     │   │
│   │ ETL pipeline│     │ SHAP explai │     │ DPDP audit  │   │
│   │ SQLite DB   │     │ 300-900 scr │     │ Anomaly det │   │
│   └─────────────┘     └─────────────┘     └─────────────┘   │
│          │                   │                   │            │
│          └───────────────────┴───────────────────┘            │
│                              │                                │
│                    ┌─────────▼─────────┐                     │
│                    │  STREAMLIT        │                     │
│                    │  DASHBOARD        │                     │
│                    │                   │                     │
│                    │  Screen 1: Score  │                     │
│                    │  Screen 2: SHAP   │                     │
│                    │  Screen 3: Security│                    │
│                    │  Screen 4: Audit  │                     │
│                    └───────────────────┘                     │
│                              │                                │
│                    ┌─────────▼─────────┐                     │
│                    │  STREAMLIT CLOUD  │                     │
│                    │  (Public URL)     │                     │
│                    │  Recruiter clicks │                     │
│                    │  and explores live│                     │
│                    └───────────────────┘                     │
└──────────────────────────────────────────────────────────────┘
```

---

## 6. LLD — LOW LEVEL DESIGN

### 6.1 Data Schema (SQLite)

```sql
-- Main user table (PII fields encrypted)
CREATE TABLE users (
    user_id              TEXT PRIMARY KEY,    -- encrypted
    age                  INTEGER,
    state_token          TEXT,                -- tokenized, not raw
    upi_txn_count_monthly       INTEGER,
    upi_avg_txn_value           FLOAT,
    upi_failed_txn_rate         FLOAT,        -- 0.0 to 1.0
    bill_payment_consistency    FLOAT,        -- 0.0 to 1.0
    mobile_recharge_consistency FLOAT,        -- 0.0 to 1.0
    app_login_freq_weekly       INTEGER,
    app_session_duration_avg    FLOAT,        -- minutes
    income_token                TEXT,         -- tokenized
    has_bank_account            INTEGER,      -- 0 or 1
    days_since_last_upi         INTEGER,
    credit_label                INTEGER,      -- 0=good, 1=default
    consent_timestamp           TEXT,         -- DPDP requirement
    created_at                  TEXT
);

-- Access log table (for anomaly detection)
CREATE TABLE access_log (
    log_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp    TEXT,
    action       TEXT,    -- score_query / bulk_export / login
    records_accessed INTEGER,
    ip_address   TEXT,
    flagged      INTEGER  -- 0 or 1
);

-- Compliance audit log
CREATE TABLE dpdp_audit (
    audit_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date     TEXT,
    rule_name    TEXT,
    status       TEXT,    -- PASS / FAIL
    detail       TEXT
);
```

---

### 6.2 Feature Engineering (features.py)

```
INPUT COLUMNS (raw):
upi_txn_count_monthly, upi_avg_txn_value, upi_failed_txn_rate,
bill_payment_consistency, mobile_recharge_consistency,
app_login_freq_weekly, app_session_duration_avg,
has_bank_account, days_since_last_upi

DERIVED FEATURES:
payment_reliability_index  = (bill_payment_consistency * 0.5)
                           + (mobile_recharge_consistency * 0.5)

digital_activity_score     = normalize(app_login_freq_weekly)
                           * normalize(app_session_duration_avg)

upi_health_score           = (upi_txn_count_monthly / 30)
                           - (upi_failed_txn_rate * 10)
                           clipped to [0, 10]

recency_penalty            = 1 / (days_since_last_upi + 1)

FINAL FEATURE VECTOR (15 features):
[upi_txn_count_monthly, upi_avg_txn_value, upi_failed_txn_rate,
bill_payment_consistency, mobile_recharge_consistency,
app_login_freq_weekly, app_session_duration_avg,
has_bank_account, days_since_last_upi, age,
payment_reliability_index, digital_activity_score,
upi_health_score, recency_penalty, income_estimate_normalized]
```

---

### 6.3 Credit Score Conversion (score.py)

```
MODEL OUTPUT:  probability of default  P(default) → 0.0 to 1.0

SCORE FORMULA: credit_score = 300 + (1 - P(default)) * 600

BUCKET MAPPING:
750 – 900  →  Excellent   (Green)   Low Risk
650 – 749  →  Good        (Teal)    Low-Medium Risk
550 – 649  →  Fair        (Yellow)  Medium Risk
450 – 549  →  Poor        (Orange)  High Risk
300 – 449  →  Very Poor   (Red)     Very High Risk
```

---

### 6.4 Security Module (security/)

```
encrypt.py
──────────
generate_key()         → creates AES-256 key, saves to encryption.key
encrypt_field(value)   → returns encrypted hex string
decrypt_field(token)   → returns original value
Fields encrypted:       user_id, state, income_estimate

anomaly.py
──────────
Rules checked on every access_log entry:
Rule 1: > 100 score queries from same IP in 10 mins  → HIGH alert
Rule 2: bulk_export > 500 records in one session     → HIGH alert
Rule 3: > 3 login IPs for same user in 1 hour        → MEDIUM alert
Rule 4: any query before 6am or after 11pm           → LOW alert
Output: flagged=1 in access_log + entry in anomaly_alerts.csv

dpdp_audit.py
─────────────
8 rules checked, each returns PASS or FAIL:
Rule 1: consent_timestamp exists for all users
Rule 2: PII fields are encrypted (check encryption.key exists)
Rule 3: access_log table exists and is populated
Rule 4: No raw PII in any log file (scan logs for patterns)
Rule 5: Records older than 24 months flagged for archival
Rule 6: income and state stored as tokens not raw values
Rule 7: audit trail exists for all bulk exports
Rule 8: anomaly detection is active (anomaly.py imported)
Output: dpdp_report.json with score X/8
```

---

### 6.5 Streamlit Dashboard Screens (app.py)

```
SCREEN 1 — Credit Score
  Input:   User ID text box + Submit button
  Output:  Plotly gauge chart (300–900)
           Risk bucket badge (color coded)
           Top 3 positive factors (SHAP)
           Top 3 negative factors (SHAP)
           Plain English explanation string

SCREEN 2 — Explainability
  Input:   Same user from Screen 1
  Output:  SHAP waterfall chart for that user
           Bar chart: global feature importance (top 10)
           Table: all features + their SHAP contribution

SCREEN 3 — Security Monitor
  Metric cards (auto-refresh every 60s):
    Total records encrypted today
    Anomalies flagged (red badge if > 0)
    DPDP compliance score  X / 8
    Last anomaly event timestamp
  Table: last 10 access_log entries with flag status

SCREEN 4 — DPDP Audit
  8 rules displayed as checklist
  PASS = green tick, FAIL = red cross
  Overall compliance score prominent at top
  Last audit run timestamp
  Download button → exports dpdp_report.json
```

---

## 7. SCOPE OF WORK — 4 DAY POC PLAN

### Day 1 — Data + Pipeline
```
Morning:
  - generate_data.py  → 50K synthetic users using Faker
  - etl.py            → clean + validate + load to SQLite

Afternoon:
  - features.py       → engineer all 15 features
  - Verify: SELECT COUNT(*) FROM users returns 50000
```

### Day 2 — Model + Explainability
```
Morning:
  - train.py          → train XGBoost, save model.pkl
  - Target: AUC > 0.83 on test set
  - score.py          → convert probability to 300-900 score

Afternoon:
  - explain.py        → SHAP integration
  - Test: explain_user(user_id) returns top 3 factors
  - Save: shap_summary.png for GitHub README
```

### Day 3 — Security Layer
```
Morning:
  - encrypt.py        → AES-256 on user_id, state, income
  - anomaly.py        → 4 rules, logs to access_log table

Afternoon:
  - dpdp_audit.py     → 8 DPDP rules, output dpdp_report.json
  - Target: 8/8 compliance on your own pipeline
```

### Day 4 — Dashboard + Deploy
```
Morning:
  - app.py            → build all 4 Streamlit screens
  - Test locally on localhost:8501

Afternoon:
  - Push to GitHub    → clean repo, good README
  - Deploy Streamlit Cloud → get public URL
  - Test live URL works from mobile browser
  - Screenshot all 4 screens for LinkedIn post
```

---

## 8. WHAT TO SHOW RECRUITERS

**The 30-second pitch:**
> "I built a credit scoring system for India's unbanked population using UPI and behavioral data — with a full cybersecurity layer that's DPDP compliant. Here's the live demo link."

**Three things that make them stop scrolling:**
1. Live Streamlit URL — they can play with it themselves
2. Screen 3 (Security Monitor) — nobody else has this
3. DPDP 8/8 compliance — directly solves their 2026 regulatory headache

---

*SecureScore POC | Built by Sakshi Singh | July 2026*
