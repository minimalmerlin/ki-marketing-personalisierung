import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("bank-full.csv", sep=',')

df = df.replace("unknown", pd.NA)

if "duration" in df.columns:
    df = df.drop(columns=["duration"])

y = df['Target'].map({'no': 0, 'yes': 1})
X = df.drop(columns=['Target'])

cat_cols = X.select_dtypes(include=["object", "string"]).columns
X[cat_cols] = X[cat_cols].astype("category")


X_encoded = pd.get_dummies(X, drop_first=True)

num_cols = X_encoded.select_dtypes(include=["int64", "float64"]).columns
scaler = StandardScaler()
X_encoded[num_cols] = scaler.fit_transform(X_encoded[num_cols])

print(y.value_counts(normalize=True))
