import pandas as pd

file_path = "results-20260401-135334 - results-20260401-135334.csv"

df = pd.read_csv(file_path)

print(df.head())

print(df.columns)
print(df.isnull().sum())
print(df.dtypes)
len(df)
