Dataset Overview
Source: American Bankruptcy Dataset ( american_bankruptcy.csv)

Coverage: 78, 682 company-year observations spanning 1999–2018 (73, 462 aliverecords; 5, 220 failedrecords)

Core Fields: 18 raw income-statement and balance-sheet metrics ( total_assets, , , , , , , , , , etc. ) plus company status labels ( / ). total_liabilities current_assets current_liabilities net_income ebit ebitda total_revenue retained_earnings market_valuealivefailed

Key Components
1. Python ETL & Feature Engineering ( python/main.py)
Standardized raw column names and handled missing/infinite ratio edge cases.

Engineered core financial health ratios across liquidity,leverage,profitability,and efficiency:

Liquidity: working_capital, working_capital_to_assets, current_ratio

Leverage: debt_to_assets, lt_debt_to_liabilities

Profitability & Solvency: roa, gross_margin, ebit_margin, retained_earnings_to_assets

Efficiency: asset_turnover

Computed company-level longitudinal features: first_fail_year, years_to_first_fail,consecutive-year flags,and year-over-year (YoY) deltas for revenue growth,net income,and debt-to-assets.

2. MySQL Star Schema & Analytical SQL ( sql/)
Designed a normalized star schema bankruptcy_analyticsconsisting of dim_company, , and . dim_yearfact_company_financials

Built a batch ETL pipeline ( python/load_to_mysql.py) via pymysqlto populate all 78, 682 records.

Wrote analytical SQL queries ( sql/02_analytical_queries.sql) comparing alivevs. financial averages, ranking high-leverage distressed firms, and computing 3-year rolling average ROA using SQL window functions ( ). failedAVG() OVER (PARTITION BY ...)

3. Interactive Power BI Dashboard ( powerbi/bankruptcy_dashboard.pbix)
Page 1 — All Companies (Macro Overview): Tracks total companies,company-year volume,total revenue,total assets,failure counts,and multi-year trends across 1999–2018.

Page 2 — Alive Companies (Healthy Operating Drivers):Analyzes correlations between operating margins (ebit_margin),asset efficiency (asset_turnover),liquidity buffers,androa.

Page 3 — Failed Companies (Distress Signals & Countdown): Examines leverage buildup ( debt_to_assets), negative roa, shrinking retained earnings, and the 5-year pre-failure trajectory ( years_to_first_failfrom 5down to 0).

Custom DAX Measures: Implemented size-weighted financial ratios ( Weighted Debt to Assets, , , ) to avoid distortion from small-denominator outliers. Weighted Current Ratio Weighted ROA Weighted EBIT Margin

4. Machine Learning Risk Prediction ( python/predict_bankruptcy.py)
Trained aRandomForestClassifierpipeline (SimpleImputer+ balanced class weights) using a strictout-of-time split(trained on1999–2014,evaluated on 2015–2018) with target-leakage columns excluded.

Scored the most recent fiscal year of every currently alivecompany to generate predicted_fail_proband assign Low Risk, , and tiers ( ). Medium RiskHigh Riskfuture_failure_predictions.csv
