import pandas as pd
import ast

datasmell = pd.read_csv('output/output_dsd_refactored.csv')
datasets = pd.read_csv('input/paths_refactored.csv')

for i in range(len(datasets)):

    dataset = pd.read_csv(datasets['path'][i])
    print(datasets['path'][i])
    datasmells = datasmell[datasmell['name'] == datasets['name'][i]][['attribute','Data Smell Type','Faulty Element Overview']]

    for attribute in dataset:
         print(attribute)
         if attribute in datasmells["attribute"].values:
            smell_type = datasmells[datasmells["attribute"] == attribute]["Data Smell Type"].values[0]

            if smell_type == "Extreme Value Smell":
                values = ast.literal_eval(datasmells[datasmells["attribute"] == attribute]['Faulty Element Overview'].values[0])
                max_value = dataset.loc[~dataset[attribute].isin(values)][attribute].max()
                min_value = dataset.loc[~dataset[attribute].isin(values)][attribute].min()
                dataset[attribute] = dataset[attribute].clip(lower=min_value, upper=max_value)
                #print(attribute, dataset[attribute].values)

            elif smell_type == "Missing Value Smell":
                mode_value = dataset[attribute].mode()
                
                if not mode_value.empty:
                    mode_value = mode_value.iloc[0]
                    dataset[attribute].fillna(mode_value, inplace=True)
                else:
                    dataset.drop(columns=[attribute], inplace=True)
                        #print(attribute, dataset[attribute].values)

            elif smell_type == "Suspect Sign Smell":
                values = ast.literal_eval(datasmells[datasmells["attribute"] == attribute]['Faulty Element Overview'].values[0])
                max_value = dataset.loc[~dataset[attribute].isin(values)][attribute].max()
                min_value = dataset.loc[~dataset[attribute].isin(values)][attribute].min()
                dataset[attribute] = dataset[attribute].clip(lower=min_value, upper=max_value)
                #print(attribute, dataset[attribute].values)

    dataset.to_csv(datasets['path'][i], index=False)
    print(datasets['name'][i] + " refactored")