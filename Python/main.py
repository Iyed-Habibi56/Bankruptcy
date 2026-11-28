import pandas as pd
import numpy as np

df = pd.read_csv("american_bankruptcy.csv")
rename_map = {
    "X1": "current_assets",
    "X2": "cost_of_goods_sold",
    "X3": "depreciation_amortization",
    "X4": "ebitda",
    "X5": "inventory",
    "X6": "net_income",
    "X7": "total_receivables",
    "X8": "market_value",
    "X9": "net_sales",
    "X10": "total_assets",
    "X11": "long_term_debt",
    "X12": "ebit",
    "X13": "gross_profit",
    "X14": "current_liabilities",
    "X15": "retained_earnings",
    "X16": "total_revenue",
    "X17": "total_liabilities",
    "X18": "operating_expenses",
}

df = df.rename(columns=rename_map)
print("Columns after rename:", df.columns.tolist())
df = df.sort_values(["company_name", "year"]).reset_index(drop=True)

def safe_div(num, den):
    return np.where((den.notna()) & (den != 0), num / den, np.nan)

df["working_capital"] = df["current_assets"] - df["current_liabilities"]
df["working_capital_to_assets"] = safe_div(df["working_capital"], df["total_assets"])

df["current_ratio"] = safe_div(df["current_assets"], df["current_liabilities"])
df["debt_to_assets"] = safe_div(df["total_liabilities"], df["total_assets"])
df["lt_debt_to_liabilities"] = safe_div(df["long_term_debt"], df["total_liabilities"])

df["retained_earnings_to_assets"] = safe_div(df["retained_earnings"], df["total_assets"])
df["roa"] = safe_div(df["net_income"], df["total_assets"])
df["gross_margin"] = safe_div(df["gross_profit"], df["net_sales"])
df["ebit_margin"] = safe_div(df["ebit"], df["total_revenue"])
df["asset_turnover"] = safe_div(df["net_sales"], df["total_assets"])


grouped = df.groupby("company_name")
df["prev_year"] = grouped["year"].shift(1)
df["is_consecutive_year"] = (df["year"] - df["prev_year"]) == 1

prev_rev = grouped["total_revenue"].shift(1)
df["yoy_revenue_growth"] = np.where(df["is_consecutive_year"] & (prev_rev.notna()) & (prev_rev != 0),(df["total_revenue"] - prev_rev) / prev_rev.abs(),np.nan,)
df["yoy_net_income_delta"] = np.where(df["is_consecutive_year"],df["net_income"] - grouped["net_income"].shift(1),np.nan,)
df["yoy_debt_to_assets_delta"] = np.where(df["is_consecutive_year"],df["debt_to_assets"] - grouped["debt_to_assets"].shift(1),np.nan,)

first_fail_year = (df[df["status_label"] == "failed"].groupby("company_name")["year"].min())

df["first_fail_year"] = df["company_name"].map(first_fail_year)
df["years_to_first_fail"] = df["year"] - df["first_fail_year"]

df = df.drop(columns=["prev_year"])
df.to_csv("american_bankruptcy_clean.csv", index=False)
print("Done! Saved american_bankruptcy_clean.csv with shape:", df.shape)
