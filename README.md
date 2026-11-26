# US Corporate Bankruptcy Analytics & Risk Prediction (1999–2018)

An end-to-end **Python**, **MySQL**, **Power BI**, and **Machine Learning** project analyzing corporate financial distress across **78,682 US company-year records** (`1999–2018`).

---

## Repository Structure

```text
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

Dataset Overview
Dataset: ( company-year rows across ) american_bankruptcy.csv78,6821999–2018

Status Breakdown: records and records 73,462 alive5,220 failed

Features & Ratios: 18 core financial statement metrics ( total_assets, , , , , , , , , , , etc. ) plus engineered ratios ( , , , , , , ) and year-over-year ( ) changes. total_liabilities current_assets current_liabilities net_income ebit ebitda total_revenue retained_earnings market_valuedebt_to_assets current_ratio roa ebit_margin asset_turnover working_capital_to_assets retained_earnings_to_assetsYoY

Project Walkthrough
1. Python Data Pipeline & Machine Learning ( python/& data/)
python/main.py: Cleans raw financial records, handles edge cases, engineers liquidity/leverage/profitability/efficiency ratios, computes longitudinal failure timelines ( first_fail_year, ), and calculates shifts. years_to_first_failYoY

python/load_to_mysql.py: Connects to MySQL with pymysqland batch-loads the processed company-year records into the database.

python/prediction.py: Trains a RandomForestClassifierwith median imputation and balanced class weights using a time-based split ( 1999–2014train, test) while excluding target-leakage columns ( , ). Scores the latest year of currently companies and outputs ( and / / tiers). 2015–2018first_fail_year years_to_first_failalivedata/future_failure_predictions.csvpredicted_fail_probLow RiskMedium RiskHigh Risk

2. MySQL Star Schema & Analytical SQL ( sql/)
sql/create_schema.sql: Defines the bankruptcy_analyticsstar schema ( dim_company, , and ). dim_yearfact_company_financials

sql/alive_vs_failed_company.sql: Contrasts liquidity, profitability, and solvency indicators across healthy vs. distressed companies.

sql/avg_ROA.sql: Tracks profitability trends and multi-year rolling averages over time.

sql/debt_to_assets.sql: Highlights high-leverage companies and pre-bankruptcy debt accumulation.

3. Interactive Power BI Reporting ( powerbi/Bankruptcy.pdf)
Page 1 — All Companies: Overall scale, company and company-year totals, revenue/asset trends, and failure counts.

Page 2 — Alive Companies: Relationships between operating margins, asset turnover, liquidity buffers, and ROA.

Page 3 — Failed Companies: Leverage pressure, negative returns, shrinking retained earnings, and the pre-failure countdown ( years_to_first_failfrom 5down to 0) alongside size-weighted DAX measures.

How to Run
Install required Python packages:

Bash
pip install pandas numpy pymysql scikit-learn
Run data cleaning and feature engineering:

Bash
python python/main.py
Initialize the MySQL schema and load data:

Runsql/create_schema.sqlin MySQL Workbench.

Configure your database credentials inpython/load_to_mysql.pyand run:

Bash
python python/load_to_mysql.py
Execute the SQL scripts insql/to inspect the query outputs.

Run bankruptcy risk predictions:

Bash
python python/prediction.py
View the Power BI report:

Openpowerbi/Bankruptcy.pdfdirectly in GitHub to browse all report pages.

Author
Iyed Habibi

B.Sc.Computer Science (Data Analysis Track),University of Messina

GitHub•LinkedIn
