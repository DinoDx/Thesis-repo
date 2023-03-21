from ast import List
import re
import pandas as pd
from aif360 import datasets, metrics
import great_expectations

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

print("Statistical Parity = " + str(statisticalParity))
print("Predictive Parity = " + str(predictiveParity))
print("Fairness Through Awareness = " + str(fairnessThroughAwareness[0]))

'''''
Data Smell Assessment:
    Definizione delle regole per l'analisi,
    Analisi della presenza di data smell nel dataset.
'''''

df = pd.read_csv("german_credit_data.csv")
df = df.dropna()

def _contains_casing_smell(element: str, same_case_wordcount_threshold: int) -> bool:
        same_case_wordcount_threshold = int(same_case_wordcount_threshold)
        # Extract substrings of the input string by splitting on spaces
        word_candidates: List[str] = re.split(r"\s+", element)

        words: List[str] = list()
        for word in word_candidates:
            # Find consecutive alphabetical characters. Require matching to
            # start at the begin of a string to consider cases like
            # "word." where only "word" should be extracted.
            substrings = list(re.findall(r"^[a-zA-Z]+", word))
            words = words + substrings

        word_count: int = len(words)

        # Case 1: Function for testing if all words are in lowercase
        # (e.g. "abc def ghi")
        def is_all_lower_case(word: str) -> bool:
            return word.lower() == word

        # Case 1: Function for testing if all words are in uppercase
        # (e.g. "ABC DEF GHI")
        def is_all_upper_case(word: str) -> bool:
            return word.upper() == word

        is_all_words_lowercase: bool = all(map(is_all_lower_case, words))
        is_all_words_uppercase: bool = all(map(is_all_upper_case, words))

        # At least `same_case_wordcount_threshold` lowercase or uppercase words
        # have to be present to flag a casing smell. This is required since
        # strings like "abc" should not be flagged.
        #
        # NOTE: Only consider a Casing Smell to be present if all words are
        # lower case or all are upper case. This is done to avoid that
        # inputs like "A test string" are not flagged.
        if word_count >= same_case_wordcount_threshold and \
                (is_all_words_lowercase or is_all_words_uppercase):
            return True

        # Case 2: Some words are in mixed case (e.g. "AbC dEf gHI")
        def is_mixed_case(x: str) -> bool:
            # e.g. "AbC" or "AbcDef"
            regex_case1 = r"[A-Z]+[a-z]+[A-Z]+.*"
            # e.g. "aBC" or "abCdefGHI"
            regex_case2 = r"[a-z]+[A-Z]+.*"
            regex = f"^({regex_case1}|{regex_case2})$"
            return bool(re.match(regex, x))
        return any(map(is_mixed_case, words))

for id, row in df.iterrows():
     for element in row:
        if(-_contains_casing_smell(element=str(element), same_case_wordcount_threshold=1) == -1):
            print(str(element) + " is smelly")


