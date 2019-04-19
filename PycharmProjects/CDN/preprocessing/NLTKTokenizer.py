from nltk import word_tokenize
from nltk.corpus import stopwords


class NLTKTokenizer:

    def tokenize_punct_nltk(self, s: str) -> list:
        return [word.lower for word in word_tokenize(s) if word.isalpha()]

    def remove_stopwords_nltk(self, tokens: list) -> list:
        stops = set(stopwords.words('english'))
        return [word for word in tokens if word not in stops]

    def stem_words_nltk(self, words: list) -> list:
        pass
