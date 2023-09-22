import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import words

def are_all_words_spelled_correctly(input_string):

    if not isinstance(input_string, str):
        return True
    
    word_tokens = word_tokenize(input_string)
    english_vocab = set(words.words())
    
    # Verifica ciascuna parola nell'elenco
    for word in word_tokens:
        # Verifica se la parola è scritta correttamente
        if word.lower() not in english_vocab:
            return False
    
    # Se tutte le parole sono scritte correttamente, ritorna True
    return True


def compute_consistency(df):
    total_percentages = 0
    num_columns = len(df.columns)

    for col_name in df.columns:
        # Rimuovi i valori NaN prima di calcolare il tipo più comune
        non_nan_values = df[col_name].dropna()
        most_common_type = non_nan_values.apply(type).mode()[0]
        consistent_type_values_count = (non_nan_values.apply(type) == most_common_type).sum()
        total_values_in_column = len(non_nan_values)
        percentage_consistent_type = (consistent_type_values_count / total_values_in_column) * 100
        total_percentages += percentage_consistent_type

    average_percentage = total_percentages / num_columns
    return average_percentage

def quality_assessment(path):

    df = pd.read_csv(path)

    completeness = (df.count().sum() / df.size) * 100

    uniqueness = (df.drop_duplicates().shape[0] / df.shape[0]) * 100

    consistency = compute_consistency(df)

    readability = (df.applymap(are_all_words_spelled_correctly).sum().sum() / df.size) * 100

    return completeness, uniqueness, consistency, readability

'''''
if __name__=="__main__":
    completeness, uniqueness, consistency = quality_assessment("datasets/kdd-census.csv")
    print(completeness, uniqueness, consistency)
'''''