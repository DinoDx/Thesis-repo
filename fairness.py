from aif360 import datasets, metrics
import pandas as pd

def fairness_assessment(path, label_name, favorable_classes, protected_attribute_names, privileged_classes, features_to_drop, privileged_groups, unprivileged_groups):
    df = pd.read_csv(path)
    df = df.fillna(df.mode())
    df = df.fillna("null")
    df = df.apply(lambda x: pd.factorize(x)[0] if x.dtype == object else x)

    dataset = datasets.StandardDataset(df,
                                    label_name=label_name,
                                    favorable_classes=[favorable_classes],
                                    protected_attribute_names=[protected_attribute_names],
                                    privileged_classes=[lambda x: eval(privileged_classes)],
                                    features_to_drop=[features_to_drop]
                                    )

    datasetMetrics = metrics.BinaryLabelDatasetMetric(dataset,
                                                        privileged_groups=[{privileged_groups:1}],
                                                        unprivileged_groups=[{unprivileged_groups:0}])

    statisticalParity = datasetMetrics.disparate_impact()
    predictiveParity = datasetMetrics.statistical_parity_difference()
    fairnessThroughAwareness = datasetMetrics.consistency()

    return statisticalParity, predictiveParity, fairnessThroughAwareness