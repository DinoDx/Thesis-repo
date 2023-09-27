import pandas as pd
from dataSmellDetection import smell_detection
from fairnessMetricsComputation import fairness_assessment
from qualityMetricsComputation import quality_assessment



meta_dataset = pd.read_csv('input/meta_dataset.csv')
paths = pd.read_csv('input/paths_refactored.csv')
fairness = pd.DataFrame()
smells = pd.DataFrame()
quality = pd.DataFrame()

for i in range(len(paths)):
    temp_smells = smell_detection(paths['path'][i])
    temp_smells['name'] = paths['name'][i]
    smells = pd.concat([smells, temp_smells])

    temp_quality = quality_assessment(paths['path'][i])
    temp_quality['name'] = paths['name'][i]
    quality = pd.concat([quality, temp_quality])


for i in range(len(meta_dataset)):

    disparateImpact, statisticalParityDifference, consistency = fairness_assessment(
        path=meta_dataset['path'][i].replace('.csv', '_refactored.csv'),
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
                      'Disparate Impact': [disparateImpact],
                      'Statistical Parity Difference': [statisticalParityDifference],
                      'Consistency': [consistency.item()]})
    ], ignore_index=True)

    
print(smells)
print(fairness)
print(quality)

smells.to_csv("output/output_dsd_refactored.csv", index=False)
fairness.to_csv("output/output_aif360_refactored.csv", index=False)
quality.to_csv("output/output_quality_refactored.csv", index=False)