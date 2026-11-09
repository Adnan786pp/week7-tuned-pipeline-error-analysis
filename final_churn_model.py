import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import precision_recall_curve, classification_report
from xgboost import XGBClassifier

df = pd.read_csv("churnguard_processed.csv")
if 'TotalCharges' in df.columns:
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].replace(' ', np.nan), errors='coerce')
if 'SeniorCitizen' in df.columns:
    df['SeniorCitizen'] = df['SeniorCitizen'].astype(str)

target_col = 'Churn'
drop_cols = ['customerID', target_col] if 'customerID' in df.columns else [target_col]
X = df.drop(columns=[col for col in drop_cols if col in df.columns])
y = df[target_col].map({'Yes': 1, 'No': 0}) if df[target_col].dtype == 'O' else df[target_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X_train.select_dtypes(include=['object']).columns.tolist()

num_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
cat_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))
])
preprocessor = ColumnTransformer([
    ('num', num_transformer, num_cols),
    ('cat', cat_transformer, cat_cols)
])

scale_weight = (len(y_train) - sum(y_train)) / sum(y_train)

full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(scale_pos_weight=scale_weight, random_state=42, eval_metric='logloss'))
])

n_est_values = list(range(50, 201, 50))
m_dep_values = list(range(3, 8, 2))
l_rat_values = [float(x)/100 for x in range(1, 22, 5)]
sub_s_values = [float(x)/10 for x in range(6, 11, 2)]
col_s_values = [float(x)/10 for x in range(6, 11, 2)]

param_distributions = {
    'classifier__n_estimators': n_est_values,
    'classifier__max_depth': m_dep_values,
    'classifier__learning_rate': l_rat_values,
    'classifier__subsample': sub_s_values,
    'classifier__colsample_bytree': col_s_values
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
search = RandomizedSearchCV(full_pipeline, param_distributions=param_distributions, n_iter=3, scoring='f1', cv=cv, random_state=42, n_jobs=-1)
search.fit(X_train, y_train)

best_model = search.best_estimator_
y_probs = best_model.predict_proba(X_test)[:, 1]
precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)

idx = np.where(recalls >= 0.80)
chosen_threshold = float(thresholds[idx[-1]]) if len(idx) > 0 else 0.32
y_pred_custom = (y_probs >= chosen_threshold).astype(int)

print(f"🎯 Deployment Operating Threshold: {chosen_threshold:.4f}")
print(classification_report(y_test, y_pred_custom))
