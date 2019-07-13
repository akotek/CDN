import operator
from abc import ABC
from functools import reduce


class Query(ABC):

    def is_empty(self) -> bool:
        return True


class BoolQuery(Query):

    # Defines a string boolean search query in the form of
    # (....) predicate (....) ....
    # Includes must (==AND), must_not(==NOT) and should (==OR)

    # Nested query can be represented as nested must/must_not/should:
    # ('a' AND 'b') OR ('c' AND 'd')
    # >> should ( [ must(['a', 'b']), must(['c', 'd']) ] )

    def __init__(self, must: list = None, must_not: list = None, should: list = None):
        self.must = self.init(must)
        self.must_not = self.init(must_not)
        self.should = self.init(should)

    def add_must(self, must: str):
        self.must.append(must)

    def add_must_not(self, must_not: str):
        self.must_not.append(must_not)

    def add_should(self, should: str):
        self.should.append(should)

    def init(self, v):
        return [] if v is None else v

    def is_empty(self) -> bool:
        return not self.must and not self.must_not and not self.should

    def get_all(self) -> list:
        return reduce(operator.concat, [self.must, self.should, self.must_not])


class PhraseQuery(Query):

    # Represents a phrase query to perform 'proximity search' with a slop (distance) defaulted to ==1
    # Queries syntax includes only AND search for now:
    # "pink ink" >> search for documents containing both words in near (1) position

    def __init__(self, terms: list, slop: int=1):
        self.terms = terms
        self.slop = slop

    def is_empty(self) -> bool:
        return not self.terms