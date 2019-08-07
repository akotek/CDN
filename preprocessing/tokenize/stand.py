from preprocessing.tokenize.tokenizer import Tokenizer


class StandardTokenizer(Tokenizer):

    def tokenize(self, s: str, stops: set=None, stops_file: str=None) -> list:
        # The standard tokenizer provides grammar based tokenize,
        # it removes whitespaces, punctuation, duplications and lower cases tokens

        # The standard tokenizer accepts the following parameters:
        # s: The string to tokenize.
        # stops: A pre-defined stop words list Defaults to the empty set.
        # stops_file: The path to a file containing stop words.

        # "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
        # >> [ the, 2, quick, brown, foxes, jumped, over, the, lazy, dog's, bone ]

        if stops_file:
            stops = self._build_stops(stops_file)

        return super().tokenize(s.lower(), stops)

    def _build_stops(self, sf):
        stops = set()
        with open(sf, 'r') as f:
            for line in f:
                stops.add(line.rstrip())
        return stops
