import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

smells= pd.read_csv('output/output_dsd.csv')
fairness = pd.read_csv('output/output_aif360.csv')
quality = pd.read_csv('output/output_quality.csv')
final = pd.read_csv('final.csv')

merged_df = smells.merge(quality, on=['name', 'attribute'])
result = merged_df.pivot(index=['attribute', 'name'], columns='Data Smell Type', values=['Faulty Element Count']).reset_index()
result.columns = ['attribute', 'name'] + [f'{col[0]}_{col[1]}' for col in result.columns[2:]]
merged_df = pd.merge(result, merged_df[['attribute', 'name', 'completeness', 'uniqueness', 'consistency', 'readability']], on=['attribute', 'name'], how='left')
merged_df = merged_df.fillna(0)
merged_df = merged_df.drop_duplicates()

'''''
# for fairness metrics regression
merged_df = smells.merge(fairness, on=['name', 'attribute'])
result = merged_df.pivot(index=['attribute', 'name'], columns='Data Smell Type', values=['Faulty Element Count']).reset_index()
result.columns = ['attribute', 'name'] + [f'{col[0]}_{col[1]}' for col in result.columns[2:]]
merged_df = pd.merge(result, merged_df[['attribute', 'name', 'Disparate Impact', 'Statistical Parity Difference', 'Consistency']], on=['attribute', 'name'], how='left')
merged_df['Faulty Element Count_Suspect Sign Smell'] = 0.0
merged_df = merged_df.fillna(0)
merged_df = merged_df.drop_duplicates()
'''''

x1 = merged_df['Faulty Element Count_Extreme Value Smell']
x2 = merged_df['Faulty Element Count_Missing Value Smell']
x3 = merged_df['Faulty Element Count_Suspect Sign Smell']


#y = merged_df['Disparate Impact']
#y = merged_df['Statistical Parity Difference']
#y = merged_df['Consistency']
y = merged_df['completeness']
#y = merged_df['uniqueness']
#y = merged_df['consistency']
#y = merged_df['readability']

data = pd.DataFrame({'x1': x1, 'x2' : x2, 'x3': x3, 'Consistency': y})
data = sm.add_constant(data)
model = sm.OLS(data['Consistency'], data[['const', 'x1', 'x2', 'x3']]).fit()
print(model.summary2())


