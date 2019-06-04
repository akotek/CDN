from preprocessing.tokenize.tokenizer import Tokenizer
from os import listdir, path


class Posting:

    # Represents a Posting in the inverted index, each posting includes it
    # document id, positions in the document and it frequency (num of times term appeared in doc)

    def __init__(self, id: int, pos_list: list = None):
        self.id = id
        self.pos_list = [] if not pos_list else pos_list
        self.tf = 0 if not pos_list else len(pos_list)

    def __repr__(self):
        return "{},{}: [{}]".format(self.id, self.tf, ','.join(map(str, self.pos_list)))

    def __str__(self):
        return "\t{}".format(self.__repr__())


class Term:

    # Represents a Term in the inverted index,
    # Each term has document-frequency (num of docs term appeared in) and posting list

    def __init__(self, pst_list: list = None):
        self.pst_list = pst_list
        self.df = 0 if not pst_list else sum(p.tf for p in pst_list)

    def add_post(self, id, pos):

        # Adds post to posts list,
        # if exists: increments it df

        post = next((p for p in self.pst_list if p.id == id), None)
        if not post:
            post = Posting(id, [pos])
            self.pst_list.append(Posting(id, [pos]))

        post.pos_list.append(pos)
        self.df, post.tf = self.df + 1, post.tf + 1


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
                dstr = "".join(doc.readlines()).replace("\n", " ")
                for tok, pos in self.tokenizer.tokenize(dstr):
                    if tok not in index:
                        index[tok] = Term([Posting(n, [pos])])
                    else:
                        index.get(tok).add_post(n, pos)
        return index
