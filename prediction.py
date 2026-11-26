import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.pipeline import Pipeline


df = pd.read_csv("american_bankruptcy_clean.csv")

# 2. Define the binary target: 1 = failed, 0 = alive
df["target_failed"] = (df["status_label"] == "failed").astype(int)

# 3. Select financial & YoY features (strictly excluding leakage columns like first_fail_year)
feature_cols = [
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
    "yoy_revenue_growth",
    "yoy_net_income_delta",
    "yoy_debt_to_assets_delta",
]

# Replace any remaining infinities with NaN so the imputer handles them cleanly
df[feature_cols] = df[feature_cols].replace([np.inf, -np.inf], np.nan)

# 4. Time-based Train/Test Split (Train: 1999-2014 | Test: 2015-2018)
train_df = df[df["year"] <= 2014].copy()
test_df = df[df["year"] > 2014].copy()

X_train, y_train = train_df[feature_cols], train_df["target_failed"]
X_test, y_test = test_df[feature_cols], test_df["target_failed"]

# 5. Build an Imputation + Random Forest Pipeline
model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    (
        "clf",
        RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            min_samples_leaf=10,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
    ),
])

# 6. Train and evaluate on out-of-time test years (2015-2018)
model.fit(X_train, y_train)
test_probs = model.predict_proba(X_test)[:, 1]
test_preds = (test_probs >= 0.5).astype(int)

print(f"Out-of-Time ROC-AUC (2015–2018): {roc_auc_score(y_test, test_probs):.4f}\n")
print("Classification Report (Test Set):")
print(classification_report(y_test, test_preds, target_names=["alive", "failed"]))

# 7. Inspect top financial drivers of failure
importances = pd.Series(
    model.named_steps["clf"].feature_importances_, index=feature_cols
).sort_values(ascending=False)
print("\nTop 10 Most Important Financial Predictors:")
print(importances.head(10).round(4))

# 8. Predict future failure risk for currently ALIVE companies (using their latest year)
alive_companies = df[df["status_label"] == "alive"].copy()
latest_alive = (
    alive_companies.sort_values("year")
    .groupby("company_name", as_index=False)
    .last()
)

latest_alive["predicted_fail_prob"] = model.predict_proba(latest_alive[feature_cols])[:, 1]
latest_alive["risk_tier"] = pd.cut(
    latest_alive["predicted_fail_prob"],
    bins=[0.0, 0.30, 0.60, 1.0],
    labels=["Low Risk", "Medium Risk", "High Risk"],
    include_lowest=True,
)

# 9. Export predictions to CSV (can also be imported into Power BI!)
output_cols = [
    "company_name",
    "year",
    "predicted_fail_prob",
    "risk_tier",
    "debt_to_assets",
    "roa",
    "current_ratio",
    "retained_earnings_to_assets",
]
predictions_out = latest_alive[output_cols].sort_values(
    "predicted_fail_prob", ascending=False
)
predictions_out.to_csv("future_failure_predictions.csv", index=False)

print("\nTop 15 Highest-Risk Alive Companies:")
print(predictions_out.head(15).to_string(index=False))