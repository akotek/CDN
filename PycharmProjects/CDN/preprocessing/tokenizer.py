
class Tokenizer:

    # Tokenizer names and behavior is borrowed from Elasticsearch,
    # Tokenizer's will behave as same as analyzers in ES, standard_tokenizer <-> ES standard_analyzer

    # PUNCTUATION:
    # ------------------
    BASIC_PUNCTS = [',', ':', ';', '?', '!', '/', '?', '(', ')', '...']
    MEANINGFUL_PUNCTS = ["'", '-', "_"]
    PUNCT_MARKS = BASIC_PUNCTS + MEANINGFUL_PUNCTS
    GENERAL_TYPOGRPHY = ['&', '*', '@', '^', '=', '#', ':', '~']
    WORD_DIVIDERS = [" ", '.'] + GENERAL_TYPOGRPHY + ['$']
    # ------------------

    def __init__(self) -> None:
        super().__init__()

    def standard_tokenizer(self, s: str) -> list:

        # The standard tokenizer provides grammar based tokenization (based on the Unicode Text Segmentation algorithm)
        # it removes whitespaces, punctuation, duplications and lower cases tokens ('lowercase' filter)

        # "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
        # >> [ the, 2, quick, brown, foxes, jumped, over, the, lazy, dog's, bone ]

        tokens, chars = dict(), list()
        s = s.lower().strip()

        for i in range(len(s)):
            if s[i] in self.WORD_DIVIDERS:
                if chars:
                    tokens[len(tokens)] = "".join(chars)  # keys are order of insertion
                    chars = []
            elif s[i] in self.PUNCT_MARKS:
                if s[i] in self.MEANINGFUL_PUNCTS and i != len(s) - 1:
                    if s[i + 1].isalpha():
                        chars.append(s[i])
            else:
                chars.append(s[i])
        return [tokens[key] for key in sorted(tokens.keys())]

    def keyword_tokenizer(self, s: str) -> list:

        # The keyword tokenizer is a “noop” tokenizer that accepts whatever text it
        #  is given and outputs the exact same text as a single term

        # "New York"
        # >> [ New York ]

        return [s.lower()]