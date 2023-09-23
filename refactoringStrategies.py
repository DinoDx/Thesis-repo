import pandas as pd
import ast

datasmell = pd.read_csv('output/output_dsd.csv')
datasets = pd.read_csv('input/paths.csv')

for i in range(len(datasets)):

    dataset = pd.read_csv(datasets['path'][i])
    datasmells = datasmell[datasmell['name'] == datasets['name'][i]][['attribute','Data Smell Type','Faulty Element Overview']]

    for attribute in dataset:
        if attribute in datasmells["attribute"].values:
            smell_type = datasmells[datasmells["attribute"] == attribute]["Data Smell Type"].values[0]
        
            if smell_type == "Extreme Value Smell":
                values = ast.literal_eval(datasmells['Faulty Element Overview'].values[0])
                min_value = dataset.loc[~dataset[attribute].isin(values)][attribute].min()
                max_value = min(values)-1
                dataset[attribute] = dataset[attribute].clip(lower=min_value, upper=max_value)
                #print(attribute, dataset[attribute].values)

            elif smell_type == "Missing Value Smell":
                for element in dataset[attribute]:
                    if str(element) == "nan":
                        dataset = dataset.fillna("nan")
                        dataset = dataset[dataset[attribute] != "nan"]
                        if len(dataset[attribute]) > 0:
                            element = dataset[attribute].mode()[0]
                        else:
                            dataset.drop(dataset[attribute], axis=1, inplace=True)

                        #print(attribute, dataset[attribute].values)

            elif smell_type == "Suspect Sign Smell":
                values = ast.literal_eval(datasmells['Faulty Element Overview'].values[0])
                min_value = dataset.loc[~dataset[attribute].isin(values)][attribute].min()
                max_value = dataset.loc[~dataset[attribute].isin(values)][attribute].max()
                dataset[attribute] = dataset[attribute].clip(lower=min_value, upper=max_value)
                #print(attribute, dataset[attribute].values)

    dataset.to_csv(datasets['path'][i])