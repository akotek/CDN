import re
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
    # ANALYZERS:
    LEGAL_TOKEN_CHARS = ["letter", "digit", "whitespace", "punctuation", "symbol"]
    # ------------------
    # REGEX:
    REGEX_NOT_WORD, REGEX_NOT_DIGIT, REGEX_NOT_WHITESPACE = "[^a-zA-Z]", "[^0-9]", "\S"
    REGEX_NOT_PUNCTUATION = "[^!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]"
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
        if chars: tokens[len(tokens)] = "".join(chars)
        return [tokens[key] for key in sorted(tokens.keys())]

    def keyword_tokenizer(self, s: str) -> list:

        # The keyword tokenizer is a “noop” tokenizer that accepts whatever text it
        #  is given and outputs the exact same text as a single term

        # "New York"
        # >> [ New York ]

        return [s.lower()]

    def _gen_reg_from_token_chars(self, sep_lst: list) -> str:
        separators = list()
        for sep in sep_lst:
            if sep == "letter":
                separators.append(self.REGEX_NOT_WORD)
            elif sep == "digit":
                separators.append(self.REGEX_NOT_DIGIT)
            elif sep == "whitespace":
                separators.append(self.REGEX_NOT_WHITESPACE)
            elif sep == "punctuation" or sep == "symbol":
                separators.append(self.REGEX_NOT_PUNCTUATION)
        return "|".join(separators) # create an OR regex

    def edge_ngram_tokenizer(self, s: str, min_gram: int = 1, max_gram: int = 2, tok_chars: list = []) -> list:

        # The edge_ngram tokenizer first breaks text down into words whenever it encounters words from token-chars,
        # then it emits N-grams of each word where the start of the N-gram is anchored to the beginning of the word.

        # min_g, max_g = Min, max length of characters in a gram.
        # Token chars to determine which characters should be kept in tokens and
        # split on anything that isn't represented in the list.

        # "Quick Fox"
        # >> [Q, Qu]

        # "Quick2Fox" with token_chars == ["letter"], will split on "2" (~token_chars)
        # >> [Q, Qu, F, Fo]

        assert s is not None
        self._assert_grams(min_gram, max_gram, tok_chars)

        split_regex = self._gen_reg_from_token_chars(tok_chars)
        splitted = re.split(split_regex, s) if split_regex else [s]
        tokens = list()

        for word in splitted:
            cur_gram, chars, cur_idx = min_gram, list(), 0
            while cur_idx < cur_gram <= max_gram and cur_gram <= len(word):
                chars.append(word[cur_idx])
                cur_idx += 1
                if len(chars) == cur_gram:
                    tokens.append("".join(chars))
                    chars, cur_idx = list(), 0
                    cur_gram += 1

        return tokens

    def ngram_tokenizer(self, s: str, min_gram: int = 1, max_gram: int = 2, tok_chars: list = []) -> list:

        # The ngram tokenizer first breaks text down into words whenever it encounters words from token-chars,
        # then it emits N-grams of each word of the specified length.
        # N-grams are like a sliding window that moves across the word -
        # a continuous sequence of characters of the specified length

        # min_g, max_g = Min, max length of characters in a gram.
        # Character classes that should be included in a token. split on characters that don’t
        # belong to the classes specified. Defaults to [] (keep all characters).

        # "Quick Fox"
        # >> [ Q, Qu, u, ui, i, ic, c, ck, k, "k ", " ", " F", F, Fo, o, ox, x ]

        self._assert_grams(min_gram, max_gram, tok_chars)

        return []

    def _assert_grams(self, min_gram, max_gram, tok_chars):

        assert 0 < min_gram < 25, 0 < max_gram < 25
        assert min_gram <= max_gram
        assert all(tokens in self.LEGAL_TOKEN_CHARS for tokens in tok_chars)