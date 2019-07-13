import unittest, filecmp
from os.path import join, dirname

from indexer.index import Index
from preprocessing.tokenize.stand import StandardTokenizer


class TestIndexer(unittest.TestCase):

    def test_positional_indexing(self):

        indexer = Index(tokenizer=StandardTokenizer())
        fp = join(dirname(__file__), "files\indexer\\")
        index = indexer.build(fp + "docs")
        with open(fp + "positional\\result", 'w') as w:
            for term_name, term in sorted(index.items()):
                w.write("{}, {}:\n".format(term_name, term.df))
                for pst in term.pst_list:
                    w.write("{}\n".format(pst))
                w.write("\n")
        self.assertTrue(filecmp.cmp(fp + "positional\\expected", fp + "positional\\result"))