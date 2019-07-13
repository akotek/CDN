from abc import ABC, abstractmethod

from search.query.query import Query, BoolQuery, PhraseQuery


class SearchModel(ABC):

    def __init__(self, index: dict):
        self.index = index

    @abstractmethod
    def search(self, sq: Query) -> list:

        # Default impl - sq is an empty query
        # Return sorted id's from dict

        ids = set()
        for term in self.index:
            for pst in self.index[term].pst_list:
                ids.add(pst.id)
        return sorted(list(ids))


class BooleanSearch(SearchModel):

    def search(self, sq: BoolQuery) -> list:

        # Performs a search from a given query in boolean retrieval model,
        # Supports none-nested queries (for now) and returns sorted document ID's as result:

        if sq.is_empty():
            return super().search(sq)

        terms = sorted([self.index[term] for term in sq.get_all() if term in self.index], key=lambda t: t.df)
        if not terms:
            return []

        operator = self.build_operator(sq)

        result, terms = terms[0].pst_list, terms[1:]
        while terms and result:
            result = operator(result, terms[0].pst_list)
            terms = terms[1:]
        return [p.id for p in result]

    def build_operator(self, sq: BoolQuery):
        if sq.must:
            return self.intersect
        elif sq.should:
            return self.union
        else:
            return self.difference

    @staticmethod
    def intersect(p1: list, p2: list) -> list:

        # Performs linear merge of 2x sorted lists of postings,
        # Returns the intersection between them (== matched documents):

        res, i, j = list(), 0, 0
        while i < len(p1) and j < len(p2):
            if p1[i].id == p2[j].id:
                res.append(p1[i])
                i, j = i + 1, j + 1
            elif p1[i].id < p2[j].id:
                i += 1
            else:
                j += 1
        return res

    @staticmethod
    def union(p1: list, p2: list) -> list:

        # Performs simple linear union of two sorted lists
        # Optimizing due to sorting assumption, else: use python set.union

        res, i, j = list(), 0, 0
        while i < len(p1) and j < len(p2):
            if p1[i].id < p2[j].id:
                res.append(p1[i])
                i += 1
            elif p1[i].id > p2[j].id:
                res.append(p2[j])
                j += 1
            else:
                res.append(p1[i])
                i, j = i + 1, j + 1
        # Add remaining
        res += p1[i:] if i < len(p1) else p2[j:]
        return res

    @staticmethod
    def difference(p1: list, p2: list) -> list:
        doc_id2 = [p.id for p in p2]
        return [p for p in p1 if p.id not in doc_id2]


class PhraseSearch(BooleanSearch):

    def search(self, sq: PhraseQuery) -> list:

        if sq.is_empty():
            return SearchModel.search(self, sq)

        terms = sorted([self.index[term] for term in sq.terms if term in self.index], key=lambda t: t.df)
        if not terms:
            return []

        result, terms = terms[0].pst_list, terms[1:]
        while terms and result:
            result = self.pos_intersect(result, terms[0].pst_list, slop=sq.slop)
            terms = terms[1:]
        return [p.id for p in result]

    @staticmethod
    def pos_intersect(p1: list, p2: list, slop: int) -> list:

        # Iterates on both posting lists, matches document id
        # && tests if matched terms position are adjacent (|pos1 - pos2| < slop)

        res, i, j = list(), 0, 0
        while i < len(p1) and j < len(p2):
            if p1[i].id == p2[j].id:
                l, pp1, pp2 = list(), 0, 0
                pos1, pos2 = p1[i].pos_list, p2[j].pos_list
                while pp1 < len(pos1):
                    while pp2 < len(pos2):
                        if abs(pos1[pp1] - pos2[pp2]) <= slop:
                            l.append(pos2[pp2])
                        elif pos2[pp2] > pos1[pp1]:
                            break
                        pp2 += 1
                    while l and abs(l[0] - pos1[pp1]) > slop:
                        l.pop()
                    if l:
                        res.append(p1[i])
                    pp1 += 1
                i, j = i + 1, j + 1
            elif p1[i].id < p2[j].id:
                i += 1
            else:
                j += 1
        return res