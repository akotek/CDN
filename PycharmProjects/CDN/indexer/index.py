from preprocessing.tokenize.tokenizer import Tokenizer
from os import listdir, path


class Posting:
    def __init__(self, doc_id: int, freq: int):
        self.doc_id = doc_id
        self.freq = freq

    def __repr__(self):
        return "{}: {}".format(self.doc_id, self.freq)

    def __str__(self):
        return "\t{}".format(self.__repr__())

    def inc_freq(self):
        self.freq += 1


class Index:

    # Implementation of a simple in-memory indexer's,
    # based on algorithms presented in SEIRiP book

    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    def build(self, dir_path: str) -> dict:

        # Builds an inverted index from a given path file,
        # Parses directory path, tokenizes it docs and adds tokenized terms as posting list

        index, n = dict(), 0
        for fp in listdir(dir_path):
            n += 1
            with open(path.join(dir_path, fp), 'r') as doc:
                for line in doc:
                    for tok in self.tokenizer.tokenize(line):
                        if tok not in index:
                            index[tok] = [Posting(n, 1)]
                        else:
                            # Naive approach:
                            # Check all posts in posting list if doc_id exists:
                            post = next(filter(lambda x: x.doc_id == n, index.get(tok)), None)
                            if post: post.inc_freq()
                            else: index.get(tok).append(Posting(n, 1))

        return index