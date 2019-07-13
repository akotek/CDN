import unittest

from indexer.index import Index, Posting
from preprocessing.tokenize.stand import StandardTokenizer
from search.model.boolean import BooleanSearch, PhraseSearch
from search.query.query import BoolQuery, PhraseQuery
from search.query.processor import QueryProcessor


class TestBooleanSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._index = Index(tokenizer=StandardTokenizer()).build("files\indexer\\docs")

    def test_intersection(self):
        p1, p2 = (self.init_posting_from_ids(lst) for lst in [[1, 2, 4, 11, 31], [2, 31, 54]])
        result = [p.id for p in BooleanSearch.intersect(p1, p2)]
        self.assertListEqual([2, 31], result)

    def test_union(self):
        p1, p2 = (self.init_posting_from_ids(lst) for lst in [[1, 2, 4, 11], [0, 2, 11, 35]])
        result = [p.id for p in BooleanSearch.union(p1, p2)]
        self.assertListEqual([0, 1, 2, 4, 11, 35], result)

    def test_difference(self):
        p1, p2 = (self.init_posting_from_ids(lst) for lst in [[2, 4, 6, 30], [0, 3, 4, 30]])
        result = [p.id for p in BooleanSearch.difference(p1, p2)]
        self.assertListEqual([2, 6], result)

    @unittest.skip
    def test_simple_query_optimization(self):
        t1, t2, t3 = (self.init_posting_from_ids(lst) for lst in [[1, 2, 4, 11, 31, 45, 173, 174],
                                                                  [1, 2, 4, 5, 6, 16, 57, 132, 140],
                                                                  [2, 31, 54, 101]])
        # query == (t1 AND t2 AND t3):
        sorted_terms = QueryProcessor.optimize_query([t1, t2, t3])
        self.assertListEqual([t3, t1, t2], sorted_terms)

    def test_get_all_boolean_search(self):
        model = BooleanSearch(self._index)
        result = model.search(BoolQuery())
        self.assertListEqual([1, 2, 3, 4, 5], result)

    def test_and_boolean_search(self):
        t1_and = ["and", "he", "ink"]
        model = BooleanSearch(self._index)
        result = model.search(BoolQuery(t1_and))
        self.assertListEqual([5], result)

    def test_or_boolean_search(self):
        t2_or = ["wink", "ink"]
        model = BooleanSearch(self._index)
        result = model.search(BoolQuery(should=t2_or))
        self.assertListEqual([1, 3, 4, 5], result)

    @unittest.skip("think on NOT alg")
    def test_not_boolean_search(self):
        t3_not = ["drink", "and"]   # "drink" NOT "and"
        model = BooleanSearch(self._index)
        result = model.search(BoolQuery(must_not=t3_not))
        self.assertListEqual([1, 3, 4], result)

    def test_phrase_search(self):
        phrase = ["drink", "pink", "ink"]
        model = PhraseSearch(self._index)
        result = model.search(PhraseQuery(terms=phrase))
        self.assertListEqual([5], result)

    def test_phrase_search_with_slop(self):
        phrase = ["likes", "drink"]
        model = PhraseSearch(self._index)
        result = model.search(PhraseQuery(terms=phrase, slop=2))
        self.assertListEqual([1, 2, 3, 4], result)

    def test_invalid_phrase_search(self):
        phrase = ["likes", "wink"]  # (slop > 1)"
        model = PhraseSearch(self._index)
        result = model.search(PhraseQuery(terms=phrase))
        self.assertListEqual([], result)

    def init_posting_from_ids(self, l1) -> list:
        return [Posting(p1) for p1 in l1]
