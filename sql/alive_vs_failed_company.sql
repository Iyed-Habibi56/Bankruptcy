SELECT
    status_label,
    COUNT(*) AS company_years,
    ROUND(AVG(debt_to_assets), 4) AS avg_debt_to_assets,
    ROUND(AVG(current_ratio), 4) AS avg_current_ratio,
    ROUND(AVG(roa), 4) AS avg_roa
FROM fact_company_financials
GROUP BY status_label;
