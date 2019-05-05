import re
from enum import Enum, auto
from collections import OrderedDict
from nltk.corpus import stopwords


class Tokenizer:
    # Tokenizer names and behavior is borrowed from Elasticsearch,
    # Tokenizer's will behave as same as analyzers in ES, standard_tokenizer <-> ES standard_analyzer

    # ENUMS:
    # ------------------
    class TokenizerType(Enum):
        STANDARD = auto()
        UAX_EMAIL = auto()

    # ------------------

    # PUNCTUATION MARKS:
    # ------------------
    BASIC_PUNCTS = [',', ':', ';', '?', '!', '/', '?', '(', ')', '...']
    MEANINGFUL_PUNCTS = ["'", "_", "."]
    GENERAL_TYPOGRPHY = ['&', '*', '^', '=', '#', ':', '~', '@']
    WORD_DIVIDERS = [" ", "-", "$"] + GENERAL_TYPOGRPHY
    PUNCT_MARKS = BASIC_PUNCTS + MEANINGFUL_PUNCTS + WORD_DIVIDERS
    # ------------------
    # ANALYZERS:
    LEGAL_TOKEN_CHARS = ["letter", "digit", "whitespace", "punctuation", "symbol"]
    # ------------------
    # STOPWORDS:
    ENG_STOPS = set(stopwords.words('english'))
    # ------------------
    # ------------------
    # REGEX:
    REGEX_NOT_WORD, REGEX_NOT_DIGIT, REGEX_NOT_WHITESPACE = "[^a-zA-Z]", "[^0-9]", "\S"  # [^ indicates NOT
    REGEX_NOT_PUNCTUATION, REGEX_EMAIL = "[^!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", "[\w\.-]+@[\w\.-]+"

    # ------------------

    def __init__(self) -> None:
        super().__init__()

    def general_tokenizer(self, s: str, word_divider: list, meaningful: list) -> list:

        # General tokenizing algorithm,
        # iterates on given string, splits on given and adds tokens

        tokens, chars = OrderedDict(), list()
        s = s.strip()

        for i in range(len(s)):
            if s[i] in word_divider:
                if chars:
                    tokens["".join(chars)], chars = len(tokens), []  # value is the order of insertion
            elif s[i] in self.PUNCT_MARKS:
                if s[i] in meaningful and i != len(s) - 1 and (s[i + 1].isalpha() or s[i + 1].isnumeric()):
                    chars.append(s[i])
            else:
                chars.append(s[i])

        if chars: tokens["".join(chars)] = len(tokens)
        return list(tokens.keys())

    def standard_tokenizer(self, s: str) -> list:

        # The standard tokenizer provides grammar based tokenization,
        # it removes whitespaces, punctuation, duplications and lower cases tokens

        # "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
        # >> [ the, 2, quick, brown, foxes, jumped, over, the, lazy, dog's, bone ]
        assert s is not None
        return self.general_tokenizer(s.lower(), *self.__build_punct(self.TokenizerType.STANDARD))

    def keyword_tokenizer(self, s: str) -> list:

        # The keyword tokenizer is a “noop” tokenizer that accepts whatever text it
        #  is given and outputs the exact same text as a single term

        # "New York"
        # >> [ New York ]

        return [s.lower()]

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
        self.__assert_grams(min_gram, max_gram, tok_chars)

        split_regex = self.__gen_reg_from_token_chars(tok_chars)
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
        # TODO impl this
        # The ngram tokenizer first breaks text down into words whenever it encounters words from token-chars,
        # then it emits N-grams of each word of the specified length.
        # N-grams are like a sliding window that moves across the word -
        # a continuous sequence of characters of the specified length

        # min_g, max_g = Min, max length of characters in a gram.
        # Character classes that should be included in a token. split on characters that don’t
        # belong to the classes specified. Defaults to [] (keep all characters).

        # "Quick Fox"
        # >> [ Q, Qu, u, ui, i, ic, c, ck, k, "k ", " ", " F", F, Fo, o, ox, x ]

        self.__assert_grams(min_gram, max_gram, tok_chars)

        return []

    def uax_url_email_tokenizer(self, s: str) -> list:

        # The uax_url_email tokenizer is like the standard tokenizer except that
        # it recognises URLs and email addresses as single tokens.

        # "Email me at john.smith@global-international.com"
        # >> [ Email, me, at, john.smith@global-international.com ]
        # while standard tokenizer >> [ email, me, at, john.smith, global, international.com ]
        assert s is not None
        if not re.findall(self.REGEX_EMAIL, s):
            return self.standard_tokenizer(s)
        return self.general_tokenizer(s, *self.__build_punct(self.TokenizerType.UAX_EMAIL))

    def stop_words_tokenizer(self, s: str, sw_file=None, stops=ENG_STOPS, rmv_trail=True) -> list:

        # The stopwords tokenizer removes stopwords from a given string,
        # it defaults to using the _english_ stop words.

        # sw_file is a path to a stopwords file configuration.
        # each stop word should be in its own "line" (separated by a line break)

        # rmv_trailing set to false in order to not ignore the last term of a search if it is a stop word.
        # useful while using edge_ngram as a query like green a can be extended to green apple

        # "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
        # >> [2, QUICK, Brown-Foxes, jumped, lazy, dog's, bone.]

        if sw_file:
            stops = set()
            with open(sw_file, 'r') as f:
                for line in f:
                    stops.add(line.rstrip())
                return self.__stop_words_remover(s, stops, rmv_trail)
        return self.__stop_words_remover(s, stops, rmv_trail)

    # Helper private methods:
    # ----------------------------------------------------
    def __stop_words_remover(self, s: str, stops: set, rmv_trail=True):

        assert s is not None, stops is not None

        s = s.strip().split(" ")
        tokens = [tok for tok in s if tok.lower() not in stops]

        if not rmv_trail and s[-1] in stops: tokens.append(s[-1])
        return tokens

    def __gen_reg_from_token_chars(self, sep_lst: list) -> str:
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
        return "|".join(separators)  # create an OR regex

    def __build_punct(self, tok_type: TokenizerType) -> tuple:
        if tok_type == self.TokenizerType.UAX_EMAIL:
            dividers = list(filter(lambda s: s not in ['@', '-', '.'], self.WORD_DIVIDERS))
            meaningful = self.MEANINGFUL_PUNCTS + ['@', '-']
            return dividers, meaningful
        return self.WORD_DIVIDERS, self.MEANINGFUL_PUNCTS

    def __assert_grams(self, min_gram, max_gram, tok_chars):
        assert 0 < min_gram < 25, 0 < max_gram < 25
        assert min_gram <= max_gram
        assert all(tokens in self.LEGAL_TOKEN_CHARS for tokens in tok_chars)
    # ----------------------------------------------------
