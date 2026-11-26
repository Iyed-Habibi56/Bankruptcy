-- 1. Create a dedicated database for this project and select it
CREATE DATABASE IF NOT EXISTS bankruptcy_analytics;
USE bankruptcy_analytics;

-- 2. Dimension table: one row per company
CREATE TABLE dim_company (
    company_name VARCHAR(30) PRIMARY KEY,
    final_status VARCHAR(20) NOT NULL,
    first_year INT NOT NULL,
    last_year INT NOT NULL,
    years_observed INT NOT NULL,
    first_fail_year INT NULL
);

-- 3. Dimension table: one row per calendar year
CREATE TABLE dim_year (
    year INT PRIMARY KEY,
    decade VARCHAR(15) NOT NULL
);

-- 4. Fact table: company financial metrics per year
CREATE TABLE fact_company_financials (
    company_name VARCHAR(30) NOT NULL,
    year INT NOT NULL,
    status_label VARCHAR(20) NOT NULL,
    current_assets DOUBLE NULL,
    cost_of_goods_sold DOUBLE NULL,
    depreciation_amortization DOUBLE NULL,
    ebitda DOUBLE NULL,
    inventory DOUBLE NULL,
    net_income DOUBLE NULL,
    total_receivables DOUBLE NULL,
    market_value DOUBLE NULL,
    net_sales DOUBLE NULL,
    total_assets DOUBLE NULL,
    long_term_debt DOUBLE NULL,
    ebit DOUBLE NULL,
    gross_profit DOUBLE NULL,
    current_liabilities DOUBLE NULL,
    retained_earnings DOUBLE NULL,
    total_revenue DOUBLE NULL,
    total_liabilities DOUBLE NULL,
    operating_expenses DOUBLE NULL,
    working_capital DOUBLE NULL,
    working_capital_to_assets DOUBLE NULL,
    current_ratio DOUBLE NULL,
    debt_to_assets DOUBLE NULL,
    lt_debt_to_liabilities DOUBLE NULL,
    retained_earnings_to_assets DOUBLE NULL,
    roa DOUBLE NULL,
    gross_margin DOUBLE NULL,
    ebit_margin DOUBLE NULL,
    asset_turnover DOUBLE NULL,
    is_consecutive_year TINYINT(1) NULL,
    yoy_revenue_growth DOUBLE NULL,
    yoy_net_income_delta DOUBLE NULL,
    yoy_debt_to_assets_delta DOUBLE NULL,
    years_to_first_fail DOUBLE NULL,
    PRIMARY KEY (company_name, year),
    CONSTRAINT fk_fact_company FOREIGN KEY (company_name) REFERENCES dim_company(company_name),
    CONSTRAINT fk_fact_year FOREIGN KEY (year) REFERENCES dim_year(year)
);
-- Populate dim_year from distinct years in staging
INSERT INTO dim_year (year, decade)
SELECT DISTINCT
    year,
    CONCAT(FLOOR(year / 10) * 10, 's') AS decade
FROM stg_bankruptcy
ORDER BY year;

-- Populate dim_company with each company's summary & final status
INSERT INTO dim_company (company_name, final_status, first_year, last_year, years_observed, first_fail_year)
SELECT
    s.company_name,
    (
        SELECT s2.status_label
        FROM stg_bankruptcy s2
        WHERE s2.company_name = s.company_name
        ORDER BY s2.year DESC
        LIMIT 1
    ) AS final_status,
    MIN(s.year) AS first_year,
    MAX(s.year) AS last_year,
    COUNT(*) AS years_observed,
    MIN(s.first_fail_year) AS first_fail_year
FROM stg_bankruptcy s
GROUP BY s.company_name;

-- Populate fact_company_financials
INSERT INTO fact_company_financials
SELECT
    company_name,
    year,
    status_label,
    current_assets,
    cost_of_goods_sold,
    depreciation_amortization,
    ebitda,
    inventory,
    net_income,
    total_receivables,
    market_value,
    net_sales,
    total_assets,
    long_term_debt,
    ebit,
    gross_profit,
    current_liabilities,
    retained_earnings,
    total_revenue,
    total_liabilities,
    operating_expenses,
    working_capital,
    working_capital_to_assets,
    current_ratio,
    debt_to_assets,
    lt_debt_to_liabilities,
    retained_earnings_to_assets,
    roa,
    gross_margin,
    ebit_margin,
    asset_turnover,
    CASE WHEN is_consecutive_year IN (1, TRUE, 'True', 'true') THEN 1 ELSE 0 END,
    yoy_revenue_growth,
    yoy_net_income_delta,
    yoy_debt_to_assets_delta,
    years_to_first_fail
FROM stg_bankruptcy;
