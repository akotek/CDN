from preprocessing.tokenize.tokenizer import Tokenizer


class KeywordTokenizer(Tokenizer):

    def tokenize(self, s: str) -> list:
        # The keyword tokenizer is a “noop” tokenizer that accepts whatever text it
        #  is given and outputs the exact same text as a single term

        # "New York"
        # >> [ New York ]

        return [s.lower()]