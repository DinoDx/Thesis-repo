import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import words

english_vocab = set(words.words())

def are_all_words_spelled_correctly(input_string, english_vocab):
    word_tokens = word_tokenize(input_string.lower())
    for word in word_tokens:
        if word not in english_vocab:
            return False
    return True


def compute_consistency(column):
    non_nan_values = column.dropna()
    most_common_type = non_nan_values.apply(type).mode().iat[0] if not non_nan_values.empty else None
    consistent_type_values_count = (non_nan_values.apply(type) == (most_common_type or None)).sum()
    total_values_in_column = len(non_nan_values)
    
    if total_values_in_column == 0:
        return 100.0
    else:
        percentage_consistent_type = (consistent_type_values_count / total_values_in_column) * 100
        return percentage_consistent_type

def quality_assessment(path):

    df = pd.read_csv(path)
    metrics = pd.DataFrame()

    for attribute in df:
        completeness = (df[attribute].count().sum() / df[attribute].size) * 100

        uniqueness = (df[attribute].drop_duplicates().shape[0] / df[attribute].shape[0]) * 100

        consistency = compute_consistency(df[attribute])

        readability = (df[attribute].apply(lambda x: are_all_words_spelled_correctly(x, english_vocab) if isinstance(x, str) else True)
                .sum() / len(df[attribute])) * 100
        
        metrics = pd.concat([metrics,
                    pd.DataFrame({'attribute': attribute,
                         'completeness':[completeness], 
                         'uniqueness':[uniqueness], 
                         'consistency':[consistency],
                         'readability': [readability]})
                            ], ignore_index=True)
    
    return metrics

'''''
if __name__=="__main__":
    completeness, uniqueness, consistency,readability = quality_assessment("datasets/adult.csv")
    print(completeness, uniqueness, consistency, readability)
'''''
