import itertools

from os import listdir, path
from preprocessing.tokenize.tokenizer import Tokenizer


class Indexer:

    # Implementation of a simple indexer,
    # based on algorithms presented in SEIRiP book

    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    def build_simple_index(self, dir_path: str) -> dict:

        # Constructs an in-memory simple inverted indexer (hash-table) given a path of files,
        # Parses directory path, tokenizes it docs and adds tokenized terms with their appearance location:

        # DOC1 : { "He likes to wink and he" }
        # DOC2 : { "The ink he likes to drink is pink" }
        # >> { "he":1,2 ,...., "drink":2 }

        assert path.exists(dir_path)

        index, n = dict(), 0
        for fp in listdir(dir_path):
            n += 1
            with open(path.join(dir_path, fp), 'r') as doc:
                tokens = [self.tokenizer.tokenize(line) for line in doc]
                for tok in set(itertools.chain.from_iterable(tokens)):
                    if tok not in index:
                        index[tok] = [n]
                    else:
                        index.get(tok).append(n)
        return index