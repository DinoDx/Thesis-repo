import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
'''''
df = pd.read_csv("output/output_dsd_refactored.csv")

conteggio = df['Data Smell Type'].value_counts()

print(conteggio)
'''''
'''''
fairness = pd.read_csv('output/output_aif360.csv')
smells = pd.read_csv('output/output_dsd.csv')

merged_df = smells.merge(fairness, on=['name', 'attribute'])
categories_to_include = ['Extreme Value Smell', 'Missing Value Smell', 'Suspect Sign Smell']
df_filtered = merged_df.loc[merged_df['Data Smell Type'].isin(categories_to_include)]


print(df_filtered)
df_filtered.to_csv("final.csv")
'''''
'''''
conteggio = df_filtered['Data Smell Type'].value_counts()
print(conteggio)
'''''
'''''
grouped = df_filtered.groupby(['Data Smell Type', "name", 'attribute_y'])['Faulty Element Count'].sum()
print(grouped)
'''''
'''''
import pandas as pd

df = pd.read_csv('output/output_quality_refactored.csv')

df_filtered = df[~df["attribute"].str.contains("Unnamed")]

df_filtered.to_csv('output/output_quality_refactored.csv', index=False)
'''''
df = pd.read_csv("output/output_quality.csv")
df2 = pd.read_csv("output/output_quality_refactored.csv")
plt.figure(figsize=(8, 6))  # Imposta le dimensioni del grafico

# Sostituisci 'df' con il nome effettivo del tuo DataFrame e 'Colonna1' e 'Colonna2' con i nomi delle tue colonne
data_to_plot = [df['consistency'], df2['consistency']]
plt.boxplot(data_to_plot)

# Imposta le etichette sull'asse x per le colonne
plt.xticks([1, 2], ['Pre-refactoring', 'Post-refactoring'])

# Aggiungi etichette e titolo
plt.ylabel('Consistency values')
plt.title('Consistency')

# Mostra il box plot
plt.show()