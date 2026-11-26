SELECT
    f.company_name,
    f.year,
    c.first_fail_year,
    ROUND(f.debt_to_assets, 4) AS debt_to_assets,
    ROUND(f.roa, 4) AS roa
FROM fact_company_financials f
JOIN dim_company c ON f.company_name = c.company_name
WHERE f.status_label = 'failed'
ORDER BY f.debt_to_assets DESC
LIMIT 10;