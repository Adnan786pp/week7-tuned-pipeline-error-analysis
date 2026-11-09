# Business Decision & Operating Threshold Justification

### Selected Operating Threshold: 0.3200 (Prioritizing Recall)

## 1. Business Preference & Financial Rationale
In Telco customer retention management, the economic consequences of classification errors are heavily asymmetrical:
- **False Negative (FN) Cost (~$150.00):** Occurs when the model fails to identify a customer who is about to churn. The customer leaves undetected, resulting in a total loss of Customer Lifetime Value (CLV).
- **False Positive (FP) Cost (~$20.00):** Occurs when the model flags a loyal customer as a churn risk. The business pushes a retention incentive. This is a minimal cost vector.

Because an **FN is 7.5x more costly than an FP**, leaving the model at the default decision threshold of `0.50` is suboptimal.

## 2. Quantitative Metric Comparison
- **At 0.50 Default Threshold:** The model achieves balanced precision, but lets potential churners slip through (Recall ~60-65%).
- **At 0.32 Custom Optimized Threshold:** By dropping the threshold to capture individuals with a >32% calculated risk, the model successfully secures a **Recall >= 80%**.
