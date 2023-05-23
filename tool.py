import pandas as pd
from wrap import smell_detection
from fairness import fairness_assessment



file_path = 'german_credit_data.csv'

df = smell_detection(file_path)
print(df)

statisticalParity, predictiveParity, fairnessThroughAwareness = fairness_assessment(file_path)
print(statisticalParity, predictiveParity, fairnessThroughAwareness)


