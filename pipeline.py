import pandas as pd
from aif360 import datasets, metrics
from rules import contains_casing_smell, contains_missing_value_smell
'''''
Preprocessing:
    Caricamento del dataset,
    Data Cleaning per eliminare valori Null o NaN,
    Fattorizzazione per codificare attributi categorici ad attributi numerici per AIFairness 360.
'''''

df = pd.read_csv("german_credit_data.csv")
df = df.dropna()
df = df.apply(lambda x: pd.factorize(x)[0])

'''''
Fairness Assessment:
    Caricamento del dataset come class StandardDataset con definizione di attributi protetti e valori privilegiati,
    Definizione della classe di metriche definendo gruppi privilegiati e non privilegiati,
    Calcolo delle metriche di fairness.
'''''

dataset = datasets.StandardDataset(df,
                                   label_name="Risk",
                                   favorable_classes=[0],
                                   protected_attribute_names=["Age"],
                                   privileged_classes=[lambda x: x >= 25],
                                   features_to_drop=["Sex"]
                                   )

datasetMetrics = metrics.BinaryLabelDatasetMetric(dataset,
                                                     privileged_groups=[{"Age":1}],
                                                     unprivileged_groups=[{"Age":0}])

statisticalParity = datasetMetrics.disparate_impact()
predictiveParity = datasetMetrics.statistical_parity_difference()
fairnessThroughAwareness = datasetMetrics.consistency()

#print("Statistical Parity = " + str(statisticalParity))
#print("Predictive Parity = " + str(predictiveParity))
#print("Fairness Through Awareness = " + str(fairnessThroughAwareness[0]))


df = pd.read_csv("german_credit_data.csv")
casingSmell = 0
missingValueSmell = 0

for id, row in df.iterrows():
     for element in row:
        if(contains_casing_smell(element=str(element), same_case_wordcount_threshold=2) == True):
            casingSmell = 1
            #print(str(element) + " is smelly")
        if(contains_missing_value_smell(element=str(element)) == True): 
            missingValueSmell = 1


output = {"name": "German Credit Risk", "Statistical Parity": statisticalParity , "Predictive Parity": predictiveParity , "Fairness Through Awareness": fairnessThroughAwareness,
           "Casing Smell": casingSmell, "Missing Value Smell": missingValueSmell}
df = pd.DataFrame(data = output)
print(df)