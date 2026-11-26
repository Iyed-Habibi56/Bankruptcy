# US Corporate Bankruptcy Analytics & Risk Prediction (1999–2018)

An end-to-end **Python**, **MySQL**, **Power BI**, and **Machine Learning** project analyzing corporate financial distress across **78,682 US company-year records** (`1999–2018`).

---

## Repository Structure

    ├── README.md
    ├── python/
    │   ├── main.py                        # Data cleaning, ratio engineering & YoY feature pipeline
    │   ├── load_to_mysql.py               # Batch ETL pipeline loading records into MySQL via pymysql
    │   └── prediction.py                  # Out-of-time Random Forest model & future risk scoring
    ├── sql/
    │   ├── create_schema.sql              # MySQL star-schema DDL (dim_company, dim_year, fact_company_financials)
    │   ├── alive_vs_failed_company.sql    # Financial metric comparisons between alive and failed firms
    │   ├── avg_ROA.sql                    # Return on assets analysis & rolling window calculations
    │   └── debt_to_assets.sql             # Leverage & distress concentration queries
    ├── data/
    │   └── future_failure_predictions.csv # Predicted failure probabilities & risk tiers for alive firms
    └── powerbi/
        └── Bankruptcy.pdf                 # Exported multi-page Power BI report (All, Alive, and Failed views)

---

## Dataset Overview

* **Dataset:** `american_bankruptcy.csv` (`78,682` company-year rows across `1999–2018`)
* **Status Breakdown:** `73,462` `alive` records and `5,220` `failed` records
* **Features & Ratios:** 18 core financial statement metrics (`total_assets`, `total_liabilities`, `current_assets`, `current_liabilities`, `net_income`, `ebit`, `ebitda`, `total_revenue`, `retained_earnings`, `market_value`, etc.) plus engineered ratios (`debt_to_assets`, `current_ratio`, `roa`, `ebit_margin`, `asset_turnover`, `working_capital_to_assets`, `retained_earnings_to_assets`) and year-over-year (`YoY`) changes.

---

## Project Walkthrough

### 1. Python Data Pipeline & Machine Learning (`python/` & `data/`)
* **`python/main.py`:** Cleans raw financial records, handles edge cases, engineers liquidity/leverage/profitability/efficiency ratios, computes longitudinal failure timelines (`first_fail_year`, `years_to_first_fail`), and calculates `YoY` shifts.
* **`python/load_to_mysql.py`:** Connects to MySQL with `pymysql` and batch-loads the processed company-year records into the database.
* **`python/prediction.py`:** Trains a `RandomForestClassifier` with median imputation and balanced class weights using a **time-based split** (`1999–2014` train, `2015–2018` test) while excluding target-leakage columns (`first_fail_year`, `years_to_first_fail`). Scores the latest year of currently `alive` companies and outputs `data/future_failure_predictions.csv` (`predicted_fail_prob` and `Low Risk` / `Medium Risk` / `High Risk` tiers).

### 2. MySQL Star Schema & Analytical SQL (`sql/`)
* **`sql/create_schema.sql`:** Defines the `bankruptcy_analytics` star schema (`dim_company`, `dim_year`, and `fact_company_financials`).
* **`sql/alive_vs_failed_company.sql`:** Contrasts liquidity, profitability, and solvency indicators across healthy vs. distressed companies.
* **`sql/avg_ROA.sql`:** Tracks profitability trends and multi-year rolling averages over time.
* **`sql/debt_to_assets.sql`:** Highlights high-leverage companies and pre-bankruptcy debt accumulation.

### 3. Interactive Power BI Reporting (`powerbi/Bankruptcy.pdf`)
* **Page 1 — All Companies:** Overall scale, company and company-year totals, revenue/asset trends, and failure counts.
* **Page 2 — Alive Companies:** Relationships between operating margins, asset turnover, liquidity buffers, and `ROA`.
* **Page 3 — Failed Companies:** Leverage pressure, negative returns, shrinking retained earnings, and the pre-failure countdown (`years_to_first_fail` from `5` down to `0`) alongside size-weighted DAX measures.

---

## How to Run

1. **Install required Python packages:**

       pip install pandas numpy pymysql scikit-learn

2. **Run data cleaning and feature engineering:**

       python python/main.py

3. **Initialize the MySQL schema and load data:**
   * Run `sql/create_schema.sql` in MySQL Workbench.
   * Configure your database credentials in `python/load_to_mysql.py` and run:

         python python/load_to_mysql.py

   * Execute the SQL scripts in `sql/` to inspect the query outputs.

4. **Run bankruptcy risk predictions:**

       python python/prediction.py

5. **View the Power BI report:**
   * Open `powerbi/Bankruptcy.pdf` directly in GitHub to browse all report pages.

---

## Author

**Iyed Habibi**  
B.Sc. Computer Science (Data Analysis Track), University of Messina  
[GitHub](https://github.com/Iyed-Habibi56) • [LinkedIn](https://www.linkedin.com/in/iyed-habibi-4bbb4128a/)
