from preprocessing.tokenize.tokenizer import Tokenizer
import re


class NGramTokenizer(Tokenizer):

    # ------------------
    # ANALYZERS:
    LEGAL_TOKEN_CHARS = ["letter", "digit", "whitespace", "punctuation", "symbol"]
    # ------------------

    def tokenize(self, s: str, min_gram: int = 1, max_gram: int = 2, tok_chars: list=None, edges=False) -> list:
        # The ngram tokenizer first breaks text down into words whenever it encounters words from token-chars,
        # then it emits N-grams of each word of the specified length.
        # N-grams are like a sliding window that moves across the word -
        # a continuous sequence of characters of the specified length

        # min_g, max_g = Min, max length of characters in a gram.
        # Character classes that should be included in a token. split on characters that don’t
        # belong to the classes specified. Defaults to [] (keep all characters).

        # "Quick Fox"
        # >> [ Q, Qu, u, ui, i, ic, c, ck, k, "k ", " ", " F", F, Fo, o, ox, x ]

        if tok_chars is None:
            tok_chars = []

        self._assert_grams(min_gram, max_gram, tok_chars)

        if edges:
            return self._edge_ngram(s, min_gram, max_gram, tok_chars)

        return []           # TODO impl this

    def _edge_ngram(self, s: str, min_gram: int = 1, max_gram: int = 2, tok_chars: list=None) -> list:

        # The edge_ngram tokenizer first breaks text down into words whenever it encounters words from token-chars,
        # then it emits N-grams of each word where the start of the N-gram is anchored to the beginning of the word.

        # min_g, max_g = Min, max length of characters in a gram.
        # Token chars to determine which characters should be kept in tokens and
        # split on anything that isn't represented in the list.

        # "Quick Fox"
        # >> [Q, Qu]

        # "Quick2Fox" with token_chars == ["letter"], will split on "2" (~token_chars)
        # >> [Q, Qu, F, Fo]

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
        return "|".join(separators)  # create an OR regex

    def _assert_grams(self, min_gram, max_gram, tok_chars):
        assert 0 < min_gram < 25, 0 < max_gram < 25
        assert min_gram <= max_gram
        assert all(tokens in self.LEGAL_TOKEN_CHARS for tokens in tok_chars)