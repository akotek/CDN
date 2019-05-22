import unittest, os, filecmp
from indexer.indexer import *
from preprocessing.tokenize.stand import StandardTokenizer


class TestIndexer(unittest.TestCase):

    def test_simple_indexer(self):

        indexer = Indexer(tokenizer=StandardTokenizer())
        fp = os.path.join(os.path.dirname(__file__), "files\indexer\\")
        index = indexer.build_simple_index(fp + "docs")
        with open(fp + "simple\\result", 'w') as w:
            for term, posts in sorted(index.items()):
                w.write("{}: {}\n".format(term, ",".join(map(str, posts))))
        self.assertTrue(filecmp.cmp(fp + "simple\\expected", fp + "simple\\result"))