from nltk.corpus import stopwords

from preprocessing.tokenize.tokenizer import Tokenizer


class StopwordsTokenizer(Tokenizer):

    # ------------------
    # STOPWORDS:
    ENG_STOPS = set(stopwords.words('english'))
    # ------------------

    def tokenize(self, s: str, sw_file=None, stops=ENG_STOPS, rmv_trail=True) -> list:
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
                return self._stops_remover(s, stops, rmv_trail)
        return self._stops_remover(s, stops, rmv_trail)

    def _stops_remover(self, s: str, stops: set, rmv_trail=True):

        s = s.strip().split(" ")
        tokens = [tok for tok in s if tok.lower() not in stops]

        if not rmv_trail and s[-1] in stops: tokens.append(s[-1])
        return tokens
