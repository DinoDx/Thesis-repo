import pandas as pd

dsd_output = pd.read_csv('output_dsd.csv')
datasets = pd.read_csv('paths.csv')

for i in range(len(datasets)):

    dataset = pd.read_csv(datasets['path'][i])
    datasmells = dsd_output[dsd_output['name'] == datasets['name'][i]][['attribute','Data Smell Type']]

    for attribute in dataset:
        if attribute in datasmells["attribute"].values:
            smell_type = datasmells[datasmells["attribute"] == attribute]["Data Smell Type"].values[0]
        
            if smell_type == "Extreme Value Smell":
                dataset[attribute] = dataset[attribute].clip(lower=1, upper=10)
                print(attribute, dataset[attribute].values)

            elif smell_type == "Missing Value Smell":
                print(#attribute, dataset[attribute].values
                    )

            elif smell_type == "Suspect Sign Smell":
                dataset[attribute] = dataset[attribute].clip(lower=1, upper=10)
                print(attribute, dataset[attribute].values)
