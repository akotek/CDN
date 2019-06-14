from abc import ABC, abstractmethod


class Tokenizer(ABC):
    # Tokenizer names and behavior is borrowed from Elasticsearch,
    # Tokenizer's will behave as same as analyzers in ES, standard_tokenizer <-> ES standard_analyzer

    # PUNCTUATION MARKS:
    # ------------------
    BASIC_PUNCTS = [':', ';', '?', '!', '/', '?', '(', ')', '...']
    MEANINGFUL_PUNCTS = ["'", "_", ".", ","]
    GENERAL_TYPOGRPHY = ['&', '*', '^', '=', '#', ':', '~', '@']
    SYMBOLS = ["\n", "\t", "\r"]
    WORD_DIVIDERS = [" ", "-", "$"] + GENERAL_TYPOGRPHY
    PUNCT_MARKS = BASIC_PUNCTS + MEANINGFUL_PUNCTS + WORD_DIVIDERS + SYMBOLS
    # ------------------
    # REGEX:
    REGEX_NOT_WORD, REGEX_NOT_DIGIT, REGEX_NOT_WHITESPACE = "[^a-zA-Z]", "[^0-9]", "\S"  # [^ indicates NOT
    REGEX_NOT_PUNCTUATION, REGEX_EMAIL = "[^!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", "[\w\.-]+@[\w\.-]+"

    # ------------------

    def __init__(self, word_divider=WORD_DIVIDERS, meaningful_puncts=MEANINGFUL_PUNCTS):
        self._word_divider = word_divider
        self._meaningful_puncts = meaningful_puncts

    @abstractmethod
    def tokenize(self, s: str, stops: set=None) -> list:

        # General tokenizing algorithm, iterates on given string,
        # Splits on given word dividers returns tokens as list of tuples (token, position)

        if stops is None:
            stops = set()

        s = s.strip()
        tokens, chars, pos = list(), list(), 1

        for i in range(len(s)):
            if s[i] in self._word_divider:
                if chars:
                    token, chars = "".join(chars), []
                    if token not in stops:
                        tokens.append((token, pos))
                    pos += 1
            elif s[i] in self.PUNCT_MARKS:
                if s[i] in self._meaningful_puncts and i != len(s) - 1 and (s[i + 1].isalpha() or s[i + 1].isnumeric()):
                    chars.append(s[i])
            else: chars.append(s[i])

        if chars: tokens.append(("".join(chars), pos))
        return tokens