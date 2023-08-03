import pandas as pd 

df = pd.read_csv("output_dsd.csv")

conteggio = df['Data Smell Type'].value_counts()

print(conteggio)