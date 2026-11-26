SELECT
    company_name,
    year,
    ROUND(roa, 4) AS roa,
    ROUND(
        AVG(roa) OVER (
            PARTITION BY company_name
            ORDER BY year
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        4
    ) AS rolling_3yr_roa
FROM fact_company_financials
WHERE roa IS NOT NULL;