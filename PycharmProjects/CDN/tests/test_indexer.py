import unittest, os, filecmp
from os.path import join, dirname

from indexer.index import Index
from preprocessing.tokenize.stand import StandardTokenizer


class TestIndexer(unittest.TestCase):

    def test_freq_indexing(self):

        indexer = Index(tokenizer=StandardTokenizer())
        fp = join(dirname(__file__), "files\indexer\\")
        index = indexer.build(fp + "docs")
        with open(fp + "freq\\result", 'w') as w:
            for term, pst_list in sorted(index.items()):
                w.write("{}:\n".format(term))
                for pst in pst_list:
                    w.write("{}\n".format(pst))
                w.write("\n")
        self.assertTrue(filecmp.cmp(fp + "freq\\expected", fp + "freq\\result"))