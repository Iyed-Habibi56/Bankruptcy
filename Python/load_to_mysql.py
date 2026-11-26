import numpy as np
import pandas as pd
import pymysql

# 1. Load cleaned CSV
df = pd.read_csv("american_bankruptcy_clean.csv")

# 2. Convert boolean column to 0 / 1 / None
df["is_consecutive_year"] = df["is_consecutive_year"].map(
    {True: 1, False: 0, 1: 1, 0: 0}
)

# 3. Connect directly to MySQL with pymysql (replace YOUR_MYSQL_PASSWORD)
conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Iyedftw6969&",
    database="bankruptcy_analytics",
    autocommit=False,
)

try:
    with conn.cursor() as cur:
        # Clear existing data if re-running
        cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cur.execute("TRUNCATE TABLE fact_company_financials;")
        cur.execute("TRUNCATE TABLE dim_company;")
        cur.execute("TRUNCATE TABLE dim_year;")
        cur.execute("SET FOREIGN_KEY_CHECKS = 1;")

        # 4. Insert into dim_year
        years = sorted(df["year"].unique())
        year_rows = [(int(y), f"{(int(y) // 10) * 10}s") for y in years]
        cur.executemany(
            "INSERT INTO dim_year (year, decade) VALUES (%s, %s)",
            year_rows,
        )

        # 5. Insert into dim_company
        dim_company = (
            df.sort_values("year")
            .groupby("company_name", as_index=False)
            .agg(
                final_status=("status_label", "last"),
                first_year=("year", "min"),
                last_year=("year", "max"),
                years_observed=("year", "count"),
                first_fail_year=("first_fail_year", "min"),
            )
        )
        company_rows = []
        for _, r in dim_company.iterrows():
            ff_year = (
                int(r["first_fail_year"])
                if pd.notna(r["first_fail_year"])
                else None
            )
            company_rows.append((
                str(r["company_name"]),
                str(r["final_status"]),
                int(r["first_year"]),
                int(r["last_year"]),
                int(r["years_observed"]),
                ff_year,
            ))

        cur.executemany(
            """
            INSERT INTO dim_company
                (company_name, final_status, first_year, last_year, years_observed, first_fail_year)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            company_rows,
        )

        # 6. Insert into fact_company_financials in batches
        fact_cols = [
            "company_name",
            "year",
            "status_label",
            "current_assets",
            "cost_of_goods_sold",
            "depreciation_amortization",
            "ebitda",
            "inventory",
            "net_income",
            "total_receivables",
            "market_value",
            "net_sales",
            "total_assets",
            "long_term_debt",
            "ebit",
            "gross_profit",
            "current_liabilities",
            "retained_earnings",
            "total_revenue",
            "total_liabilities",
            "operating_expenses",
            "working_capital",
            "working_capital_to_assets",
            "current_ratio",
            "debt_to_assets",
            "lt_debt_to_liabilities",
            "retained_earnings_to_assets",
            "roa",
            "gross_margin",
            "ebit_margin",
            "asset_turnover",
            "is_consecutive_year",
            "yoy_revenue_growth",
            "yoy_net_income_delta",
            "yoy_debt_to_assets_delta",
            "years_to_first_fail",
        ]

        clean_fact = df[fact_cols].replace([np.inf, -np.inf], np.nan)
        fact_rows = []
        for row in clean_fact.itertuples(index=False, name=None):
            converted = []
            for idx, val in enumerate(row):
                if pd.isna(val):
                    converted.append(None)
                elif fact_cols[idx] in ("company_name", "status_label"):
                    converted.append(str(val))
                elif fact_cols[idx] in ("year", "is_consecutive_year"):
                    converted.append(int(val))
                else:
                    converted.append(float(val))
            fact_rows.append(tuple(converted))

        placeholders = ", ".join(["%s"] * len(fact_cols))
        col_list = ", ".join(fact_cols)
        sql_insert = f"INSERT INTO fact_company_financials ({col_list}) VALUES ({placeholders})"

        batch_size = 2000
        for start in range(0, len(fact_rows), batch_size):
            cur.executemany(sql_insert, fact_rows[start : start + batch_size])

    conn.commit()
    print(
        f"Success! Loaded {len(year_rows)} years, {len(company_rows)} companies, and {len(fact_rows)} fact rows."
    )

except Exception as e:
    conn.rollback()
    print("Error occurred, rolled back changes:", e)

finally:
    conn.close()
