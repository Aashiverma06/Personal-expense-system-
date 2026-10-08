# PEIS — Personal Expense Intelligence System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.0](https://img.shields.io/badge/framework-Flask%203.0-green.svg)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-orange.svg)](https://scikit-learn.org/)
[![pandas](https://img.shields.io/badge/Analytics-pandas-purple.svg)](https://pandas.pydata.org/)
[![Tests Passing](https://img.shields.io/badge/tests-12%20passed%20100%25-brightgreen.svg)]()

> An intelligent, decision-support financial management web application combining **automated transaction tracking**, **dual-engine categorization (Keyword Rule-based + Machine Learning TF-IDF/Logistic Regression)**, **statistical spending pattern analysis**, **interactive dashboards**, and **personalized proactive financial insights**.

---

## 1. System Architecture & Workflow

```text
                                PEIS ARCHITECTURE
                                
    ┌────────────────────────────────────────────────────────────────────────┐
    │                       Client Layer (Frontend)                          │
    │  HTML5 + CSS3 (Responsive Design System) + Vanilla JS (AJAX Debounced) │
    │                  Chart.js (Local Offline Bundled Engine)               │
    └───────────────────────────────────┬────────────────────────────────────┘
                                        │ HTTP / JSON REST APIs
                                        ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │                      Application Layer (Flask 3.0)                     │
    │                                                                        │
    │   ┌──────────────┐  ┌──────────────────┐  ┌────────────────────────┐  │
    │   │ Auth Routes  │  │ Dashboard Routes │  │  Transactions Routes   │  │
    │   └──────────────┘  └──────────────────┘  └────────────────────────┘  │
    │   ┌──────────────┐  ┌──────────────────┐  ┌────────────────────────┐  │
    │   │ Budget API   │  │  Reports Service │  │  Experiment Benchmark  │  │
    │   └──────────────┘  └──────────────────┘  └────────────────────────┘  │
    └───────────────────────────────────┬────────────────────────────────────┘
                                        │
                                        ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │                       Intelligence & Data Services                     │
    │                                                                        │
    │   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
    │   │ Intelligent Categorizer   │      │ Financial Analytics Engine  │   │
    │   │  • Regex Keyword Rules    │      │  • Pandas DataFrames        │   │
    │   │  • Scikit-learn Pipeline  │      │  • Month-over-Month Deltas  │   │
    │   │    (TF-IDF + LogReg)      │      │  • Z-Score Anomaly Det.     │   │
    │   │  • Hybrid Confidence Rank │      │  • Category Distribution    │   │
    │   └───────────────────────────┘      └─────────────────────────────┘   │
    │                                                                        │
    │   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
    │   │ Insights & Recommendation │      │ Research Experiment Service │   │
    │   │  • 50/30/20 Saving Health │      │  • Empirical Accuracy & F1  │   │
    │   │  • Budget Utilization Cap │      │  • Latency Benchmarking     │   │
    │   │  • Discretionary Cut Tips │      │  • Live Inference Console   │   │
    │   └───────────────────────────┘      └─────────────────────────────┘   │
    └───────────────────────────────────┬────────────────────────────────────┘
                                        │
                                        ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │                    Persistence Layer (SQLite Database)                 │
    │   Tables: users | transactions | categories | budgets | insights       │
    └────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Functional Modules

### Module 1: User Management & Authentication
* User Registration, Secure Login, and Session Termination.
* Password hashing using PBKDF2 / SHA256 via `werkzeug.security`.
* User profile customization (display name and preferred currency: ₹, $, €, £).
* 1-Click **⚡ Demo Data Seeder** that populates 30+ transactions across two months to showcase intelligence analytics immediately.

### Module 2: Transaction Management
* Comprehensive CRUD (Create, Read, Update, Delete) for Expenses and Income.
* Multi-dimensional filtering: Date range, Transaction Type, Category, Payment Method, and keyword search.
* Instant CSV Export for external accounting.
* Real-time AJAX Auto-Categorization that suggests categories while typing.

### Module 3: Intelligent Expense Categorization
* **Keyword/Rule-Based Engine:** Rapid semantic token and substring dictionary matching across 12 standard spending classes.
* **Machine Learning Engine:** Scikit-learn text processing pipeline:
  $$\text{TF-IDF Vectorizer}(\text{ngram\_range}=(1, 2)) \longrightarrow \text{Logistic Regression}(\text{class\_weight}=\text{'balanced'})$$
* **Hybrid Decision Ranker:** Combines rule certainty with probabilistic model confidence to choose the most dependable classification with full human explainability.

### Module 4: Financial Dashboard
* Real-time metric cards: Total Income, Total Expenses, Net Cashflow, Savings Rate (%).
* Month-over-month growth variance (e.g. `▲ +18.2% vs last month`).
* **Visual Data Analytics:**
  * Interactive **Category Spending Doughnut Chart** with proportional tables.
  * Multi-month **Income vs. Expense Trend Bar Chart**.
* Quick-action **Transaction Modal** accessible from the top navbar globally.

### Module 5: Budget Management & Proactive Decision Support
* Category-level budget setting per month.
* Automated real-time calculations:
  * Budget Limit vs. Actual Spending vs. Remaining Balance.
  * Utilization Percentage with dynamic visual progress meters.
  * Three-tier status alerting: `Safe (<80%)`, `Warning (80%-100%)`, `Exceeded (>100%)`.

### Module 6: Intelligent Insights & Recommendations Engine
* **Spending Trend Analysis:** Alerts on spending spikes (e.g. *"Your spending increased by 18.2% compared to last month"*).
* **Category Dominance:** Identifies single categories consuming disproportionate capital (>30%).
* **Budget Alerts:** Proactive notifications when expenses near or breach budget thresholds.
* **Personalized Recommendations:** Actionable advice (e.g. *"Trimming your Food & Dining expenses by ₹1,200/month could elevate your savings to 38%"*).
* **Statistical Anomaly Detection:** Pandas $Z$-score and distribution outlier analysis flagging expenses significantly above historical category baselines.
* **Savings Rate Milestones:** Continuous assessment against the standard 50/30/20 personal finance framework.

### Module 7: Comprehensive Financial Reports
* Multi-timeframe views: Monthly, Weekly (Last 7 Days), Daily, and Annual statements.
* Daily expense timeline trend graph.
* Summary statistics: Daily average spend, largest single expense, itemized records.
* One-click **Print / Save as PDF** styling.

### Module 8: Academic Research Experiment Module (Section 12)
* Dedicated research bench comparing:
  1. **Manual Categorization** (Human baseline)
  2. **Rule-Based Keyword Matching**
  3. **Machine Learning Categorization (TF-IDF + Classifier)**
* Empirical performance evaluated against 30 held-out real test cases:
  * Measured Accuracy (%)
  * Macro F1-Score
  * Inference Latency (milliseconds)
  * Scalability analysis
* **Interactive Live Inference Console:** Test any phrase live with side-by-side latency and probability breakdowns.

---

## 3. Technology Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend** | Python 3.10+ / Flask 3.0 | Lightweight, maintainable, modular Blueprint architecture |
| **Database** | SQLite3 | Zero-configuration, serverless, atomic transactions, ACID compliant |
| **Analytics Engine** | Pandas, NumPy | Vectorized time-series aggregation, group-by statistics, Z-score outliers |
| **Machine Learning** | Scikit-learn, Joblib | TF-IDF n-gram vectorization, probabilistic classification, persistent artifacts |
| **Data Visualization**| Chart.js (Bundled locally) | 100% offline-ready, responsive HTML5 canvas charts |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | Fast, zero NPM dependency overhead, responsive design system |
| **Testing** | Pytest | Automated end-to-end unit and integration test suite |

---

## 4. Database Schema

```sql
-- 1. Users
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    currency TEXT DEFAULT '₹',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Categories
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
    icon TEXT DEFAULT 'tag',
    color TEXT DEFAULT '#3b82f6',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(name, user_id)
);

-- 3. Transactions
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
    amount REAL NOT NULL CHECK(amount > 0),
    category TEXT NOT NULL,
    description TEXT,
    payment_method TEXT NOT NULL,
    date TEXT NOT NULL,
    is_auto_categorized INTEGER DEFAULT 0,
    categorization_method TEXT DEFAULT 'manual',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 4. Budgets
CREATE TABLE budgets (
    budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    month INTEGER NOT NULL CHECK(month BETWEEN 1 AND 12),
    year INTEGER NOT NULL CHECK(year > 2000),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, category, month, year),
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 5. Insights
CREATE TABLE insights (
    insight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    severity TEXT DEFAULT 'info',
    is_dismissed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

---

## 5. Quickstart Guide (Local Setup)

### Step 1: Clone / Navigate to Project Directory
```bash
cd PEIS
```

### Step 2: Set up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python3 run.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

### Step 5: Explore with Demo Data
1. Click **Create an account** (e.g. `demo@example.com` / `password123`).
2. Once on the Dashboard, click the **⚡ Demo Data** button in the top navbar.
3. The system will automatically populate 30+ transactions across the previous and current month, along with category budgets.
4. Review the charts, insights, anomaly flags, and budget warnings!

---

## 6. Running Automated Tests

PEIS comes with a complete test suite covering authentication, CRUD operations, budgeting, categorization algorithms, insights, and research benchmarks:

```bash
PYTHONPATH=. ./venv/bin/pytest -v
```

**Expected output:**
```
tests/test_auth.py::test_register_and_login PASSED
tests/test_auth.py::test_duplicate_registration PASSED
tests/test_auth.py::test_invalid_login PASSED
tests/test_budgets.py::test_budget_creation_and_tracking PASSED
tests/test_categorizer.py::test_rule_based_categorizer PASSED
tests/test_categorizer.py::test_ml_categorizer PASSED
tests/test_categorizer.py::test_hybrid_engine PASSED
tests/test_experiment.py::test_research_experiment_benchmark PASSED
tests/test_experiment.py::test_live_prompt_test PASSED
tests/test_insights.py::test_insights_generation PASSED
tests/test_transactions.py::test_transaction_crud PASSED
tests/test_transactions.py::test_transaction_export_csv PASSED

============================== 12 passed in 0.79s ==============================
```

---

## 7. Research Experiment & Viva Guide

### Research Problem Statement
> *"Traditional personal expense trackers rely almost exclusively on manual categorization, inducing user fatigue and high churn. While rule-based systems offer low-latency keyword heuristics, they degrade when presented with lexical variation, compound items, or novel terminology. This project evaluates whether a Machine Learning classifier using n-gram TF-IDF representations delivers superior generalization and adaptability for expense classification without sacrificing real-time interactive responsiveness."*

### Empirical Benchmark Findings (from `/experiment`)
| Method | Accuracy | Macro F1 | Average Latency | Scalability | Key Observation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Manual** | User-dependent | N/A | 3,000–5,000 ms | Poor | High abandonment, typo prone |
| **Rule-Based (Keyword)** | ~70.0% | ~0.65 | < 0.2 ms | Moderate | Fast, but completely fails on unseen keywords |
| **Machine Learning (TF-IDF + LR)** | **~90.0%** | **~0.88** | **< 1.5 ms** | **High** | Generalizes to vocabulary variations & sub-words |

### Frequently Asked Viva Questions & Answers

**Q1: Why did you choose SQLite instead of MySQL or MongoDB?**  
*Answer:* SQLite requires zero daemon configuration, operates via ACID-compliant file-based storage, has negligible overhead, and natively supports SQLite Row factories and foreign keys. For a single-user personal finance management tool, it is significantly faster and more portable than maintaining external server daemons.

**Q2: Why use TF-IDF + Logistic Regression over Deep Learning (e.g. BERT)?**  
*Answer:* Expense descriptions are short texts (typically 2 to 8 words). Heavy transformer models like BERT add hundreds of megabytes of weight files, require GPU inference, and incur 50–150ms latency. In contrast, TF-IDF with bi-grams and regularized Logistic Regression executes in under 1.5 milliseconds on CPU with a model artifact under 200KB, making it optimal for interactive web experiences.

**Q3: How does the Hybrid Engine resolve conflicts between Rule and ML?**  
*Answer:* If the rule-based keyword match has strong confidence ($\ge 80\%$), it is accepted. If both rule and ML agree on a non-miscellaneous class, confidence is boosted. If ML exhibits strong probabilistic certainty ($\ge 60\%$), it takes precedence to ensure semantic generalization.

**Q4: How does PEIS detect spending anomalies?**  
*Answer:* The `FinancialAnalyticsService` utilizes Pandas to compute category-wise historical spend distributions. An anomaly is flagged if a transaction exceeds $z > 2.0$ standard deviations above the category mean, or spikes higher than 2.5x the historical baseline.
