from preprocessing.tokenize.tokenizer import Tokenizer


class StandardTokenizer(Tokenizer):

    def tokenize(self, s: str) -> list:
        # The standard tokenizer provides grammar based tokenize,
        # it removes whitespaces, punctuation, duplications and lower cases tokens

        # "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
        # >> [ the, 2, quick, brown, foxes, jumped, over, the, lazy, dog's, bone ]

        return self._general_tokenizer(s.lower())
