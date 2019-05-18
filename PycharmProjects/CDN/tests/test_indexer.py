import unittest, os
from indexer.indexer import *

class TestIndexer(unittest.TestCase):

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        self.indexer = Indexer()


    def test_basic_indexing(self):
        path = os.path.join(os.path.dirname(__file__), "files\docs")

        index = self.indexer.build_index(path)