import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(
    r"C:\Users\shiva\OneDrive\Desktop\weiter bildung\projekt\ki-marketing-personalisierung-main\data\raw\bank_marketing\bank-additional-full.csv",
    sep=';'
)
text_cols = ['job','marital','education','default','housing','loan',
             'contact','month','day_of_week','poutcome','y']

for col in text_cols:
    df[col] = df[col].str.lower().str.strip()
df = df[df['age'].between(18, 100)]
df = df[df['duration'] > 0]
df.replace("unknown", None, inplace=True)
binary_cols = ['default','housing','loan','y']

for col in binary_cols:
    df[col] = df[col].replace({'yes':'yes', 'no':'no'})

df['month'] = df['month'].str.lower()
df['day_of_week'] = df['day_of_week'].str.lower()

num_cols = ['duration','campaign','pdays','previous',
            'emp.var.rate','cons.price.idx','cons.conf.idx',
            'euribor3m','nr.employed']

for col in num_cols:
    q1 = df[col].quantile(0.01)
    q99 = df[col].quantile(0.99)
    df = df[(df[col] >= q1) & (df[col] <= q99)]
fill_unknown_cols = ['job','marital','education','default','housing','loan']

for col in fill_unknown_cols:
    df[col] = df[col].fillna("unknown")

print(df.isna().sum())
df.info()
df.head()
for col in ['job','marital','education','default','housing','loan']:
    print(col, df[col].value_counts())
    print("-----")


