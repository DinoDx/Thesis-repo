from aif360 import datasets, metrics
import pandas as pd

def fairness_assessment(path):
    df = pd.read_csv(path)
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

    return statisticalParity, predictiveParity, fairnessThroughAwareness