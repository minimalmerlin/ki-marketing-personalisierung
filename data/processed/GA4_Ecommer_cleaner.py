import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv(r'C:\\Users\\shiva\\OneDrive\\Desktop\\weiter bildung\\projekt\\ki-marketing-personalisierung-main\\data\\processed\\GA4_Ecommer.csv')
df.isna().sum()
df['user_pseudo_id'] = df['user_pseudo_id'].astype(str)
df['event_timestamp'] = pd.to_datetime(df['event_timestamp'], unit='us')
df['event_date'] = pd.to_datetime(df['event_date'], format='%Y%m%d')
print(df['user_pseudo_id'].value_counts().head())
print(df['event_date'].head())
print(df.head())
print(df.info())
print(df.describe())




