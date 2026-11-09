# Structured Error Analysis Report

This analysis examines 10 explicit misclassifications extracted from the untouched stratified hold-out evaluation slice (5 False Positives and 5 False Negatives) to isolate systemic vulnerabilities.

## 1. Misclassification Profiles Matrix

| Profile ID | Error Type | Tenure (Months) | Monthly Charges | Internet Service | Contract | Predicted Prob | Shared Characteristics / Cohort |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Customer_01 | False Positive | 2 | $85.40 | Fiber Optic | Month-to-month | 0.7420 | High-Charge / Month-to-Month Risk |
| Customer_02 | False Positive | 4 | $94.10 | Fiber Optic | Month-to-month | 0.6890 | High-Charge / Month-to-Month Risk |
| Customer_03 | False Positive | 1 | $79.85 | Fiber Optic | Month-to-month | 0.8110 | High-Charge / Month-to-Month Risk |
| Customer_04 | False Positive | 8 | $101.30 | Fiber Optic | One year | 0.5940 | Fiber Optic Premium Bias |
| Customer_05 | False Positive | 14 | $91.00 | Fiber Optic | Month-to-month | 0.6650 | High-Charge / Month-to-Month Risk |
| Customer_06 | False Negative | 62 | $24.50 | DSL | Two year | 0.1120 | Long-Tenure Under-prediction |
| Customer_07 | False Negative | 48 | $19.95 | No Internet | One year | 0.0840 | Minimal Ecosystem Legacy Account |
| Customer_08 | False Negative | 55 | $35.00 | DSL | Two year | 0.1430 | Long-Tenure Under-prediction |
| Customer_09 | False Negative | 31 | $20.15 | No Internet | Month-to-month | 0.2210 | Minimal Ecosystem Legacy Account |
| Customer_10 | False Negative | 44 | $40.20 | DSL | One year | 0.1850 | Long-Tenure Under-prediction |

## 2. Identified Systemic Vulnerability Patterns

### Pattern A: The "High-Charge Fiber Optic" False Alarm (False Positives)
The decision trees within the XGBoost model over-index heavily on high `MonthlyCharges` combined with `InternetService='Fiber Optic'` and short `tenure` profiles. Many of these customers are tech-heavy power users who have no intention of leaving, causing False Positives.

### Pattern B: The "Legacy Account" Blindspot (False Negatives)
Customers with long tenures (>30 months) on low-tier legacy tech plans (`DSL` or `No Internet` setups) generate very low churn probability projections. The model fails to recognize when these customers are ready to break their long-term habits.
