import pandas as pd 
'''''
df = pd.read_csv("output_dsd.csv")

conteggio = df['Data Smell Type'].value_counts()

print(conteggio)
'''''

fairness = pd.read_csv('output_aif360.csv')
smells = pd.read_csv('output_dsd.csv')

merged_df = smells.merge(fairness, on=['name'])
categories_to_include = ['Extreme Value Smell', 'Missing Value Smell', 'Suspect Sign Smell']
df_filtered = merged_df.loc[merged_df['Data Smell Type'].isin(categories_to_include)]


print(df_filtered)
df_filtered.to_csv("final.csv")

conteggio = df_filtered['Data Smell Type'].value_counts()
print(conteggio)

grouped = df_filtered.groupby(['Data Smell Type', "name", 'attribute_y'])['Faulty Element Count'].sum()
print(grouped)