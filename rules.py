from ast import List
import re

def contains_missing_value_smell(element: str) -> bool:
     if(element == None or element == "NaN"):
          return True
     
     return False



def contains_casing_smell(element: str, same_case_wordcount_threshold: int) -> bool:
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