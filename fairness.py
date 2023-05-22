from aif360 import datasets, metrics
import pandas as pd

file_path = 'german_credit_data.csv'
df = pd.read_csv('german_credit_data.csv')
df = df.dropna()
df = df.apply(lambda x: pd.factorize(x)[0])
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

print("Statistical Parity = " + str(statisticalParity))
print("Predictive Parity = " + str(predictiveParity))
print("Fairness Through Awareness = " + str(fairnessThroughAwareness[0]))