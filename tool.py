import pandas as pd
from wrap import smell_detection
from fairness import fairness_assessment



meta_dataset = pd.read_csv('meta_dataset.csv')
df = pd.DataFrame()

for i in range(len(meta_dataset)):

    tempdf = smell_detection(meta_dataset['path'][i])
    tempdf['name'] = meta_dataset['name'][i]
    statisticalParity, predictiveParity, fairnessThroughAwareness = fairness_assessment(path=meta_dataset['path'][i],
                                                                    label_name=meta_dataset['label_name'][i],
                                                                    favorable_classes=meta_dataset['favorable_classes'][i],
                                                                    protected_attribute_names=meta_dataset['protected_attribute_names'][i],
                                                                    privileged_classes=meta_dataset['privileged_classes'][i],
                                                                    features_to_drop=meta_dataset['features_to_drop'][i],
                                                                    privileged_groups=meta_dataset['privileged_groups'][i],
                                                                    unprivileged_groups=meta_dataset['unprivileged_groups'][i])

    tempdf['statisticalParity'] = statisticalParity
    tempdf['predictiveParity'] = predictiveParity
    tempdf['fairnessThroughAwareness'] = fairnessThroughAwareness.item()
    df=pd.concat([df,tempdf])

print(df)
df.to_csv("output.csv")