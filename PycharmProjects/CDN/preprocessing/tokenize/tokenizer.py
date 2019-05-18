from abc import ABC, abstractmethod


class Tokenizer(ABC):
    # Tokenizer names and behavior is borrowed from Elasticsearch,
    # Tokenizer's will behave as same as analyzers in ES, standard_tokenizer <-> ES standard_analyzer

    # PUNCTUATION MARKS:
    # ------------------
    BASIC_PUNCTS = [':', ';', '?', '!', '/', '?', '(', ')', '...']
    MEANINGFUL_PUNCTS = ["'", "_", ".", ","]
    GENERAL_TYPOGRPHY = ['&', '*', '^', '=', '#', ':', '~', '@']
    WORD_DIVIDERS = [" ", "-", "$"] + GENERAL_TYPOGRPHY
    PUNCT_MARKS = BASIC_PUNCTS + MEANINGFUL_PUNCTS + WORD_DIVIDERS
    # ------------------
    # ANALYZERS:
    LEGAL_TOKEN_CHARS = ["letter", "digit", "whitespace", "punctuation", "symbol"]
    # ------------------
    # REGEX:
    REGEX_NOT_WORD, REGEX_NOT_DIGIT, REGEX_NOT_WHITESPACE = "[^a-zA-Z]", "[^0-9]", "\S"  # [^ indicates NOT
    REGEX_NOT_PUNCTUATION, REGEX_EMAIL = "[^!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", "[\w\.-]+@[\w\.-]+"
    # ------------------

    def __init__(self, word_divider=WORD_DIVIDERS, meaningful_puncts=MEANINGFUL_PUNCTS):
        self._word_divider = word_divider
        self._meaningful_puncts = meaningful_puncts

    @abstractmethod
    def tokenize(self, s: str) -> list:
        return s.split(" ")

    def _general_tokenizer(self, s: str) -> list:

        # General tokenizing algorithm,
        # iterates on given string, splits on given and adds tokens

        s = s.strip()
        tokens, chars = list(), list()

        for i in range(len(s)):
            if s[i] in self._word_divider:
                if chars:
                    tokens.append("".join(chars))
                    chars = []
            elif s[i] in self.PUNCT_MARKS:
                if s[i] in self._meaningful_puncts and i != len(s) - 1 and (s[i + 1].isalpha() or s[i + 1].isnumeric()):
                    chars.append(s[i])
            else:
                chars.append(s[i])

        if chars: tokens.append("".join(chars))
        return tokens