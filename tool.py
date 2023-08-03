import pandas as pd
from wrap import smell_detection
from fairness import fairness_assessment



meta_dataset = pd.read_csv('meta_dataset.csv')
paths = pd.read_csv('paths.csv')
fairness = pd.DataFrame()
smells = pd.DataFrame()

for i in range(len(paths)):

    temp_smells = smell_detection(paths['path'][i])
    temp_smells['name'] = paths['name'][i]
    smells = pd.concat([smells, temp_smells])


for i in range(len(meta_dataset)):

    statisticalParity, predictiveParity, fairnessThroughAwareness = fairness_assessment(
        path=meta_dataset['path'][i],
        label_name=meta_dataset['label_name'][i],
        favorable_classes=meta_dataset['favorable_classes'][i],
        protected_attribute_names=meta_dataset['protected_attribute_names'][i],
        privileged_classes=meta_dataset['privileged_classes'][i],
        features_to_drop=meta_dataset['features_to_drop'][i],
        privileged_groups=meta_dataset['privileged_groups'][i],
        unprivileged_groups=meta_dataset['unprivileged_groups'][i])

    fairness = pd.concat([
        fairness,
        pd.DataFrame({'name': [meta_dataset['name'][i]],
                      'attribute':[meta_dataset['protected_attribute_names'][i]],
                      'statisticalParity': [statisticalParity],
                      'predictiveParity': [predictiveParity],
                      'fairnessThroughAwareness': [fairnessThroughAwareness.item()]})
    ], ignore_index=True)

    
print(smells)
print(fairness)

smells.to_csv("output_dsd.csv")
fairness.to_csv("output_aif360.csv")