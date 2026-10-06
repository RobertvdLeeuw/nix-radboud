import operator
from functools import reduce
from itertools import combinations


def run_hitting_set_algorithm(conflict_sets):
    """
    Algorithm that handles the entire process from conflict sets to hitting sets

    :param conflict_sets: list of conflict sets as list
    :return: the hitting sets and minimal hitting sets as list of lists
    """

    def berge(min_hits: set[frozenset], c_set: frozenset) -> set[frozenset]:
        print("Going in:", [list(hs) for hs in min_hits], ", conflict:", list(c_set))
        min_hits = [
            [hs] if hs.intersection(c_set) else [frozenset([*hs, e]) for e in c_set]
            for hs in min_hits or [{x} for x in c_set]
        ]

        print("Updated:", [list(hit) for hits in min_hits for hit in hits])

        min_hits = [hit for hits in min_hits for hit in hits]

        print("Flattened:", [list(hs) for hs in min_hits])

        # Remove supersets
        min_hits = list(
            filter(lambda hs: not any(hs.issuperset(s) and hs != s for s in min_hits), min_hits)
        )
        print("Pruned supers:", [list(hs) for hs in min_hits], "\n\n")

        return min_hits

    hitting_sets = reduce(berge, {frozenset(s) for s in conflict_sets}, set())
    hitting_sets = [list(hs) for hs in hitting_sets]

    min_k = min(map(len, hitting_sets))
    min_hitting_sets = [hs for hs in hitting_sets if len(hs) == min_k]

    return hitting_sets, min_hitting_sets


a, b = run_hitting_set_algorithm([[1, 2, 3], [3, 4, 9], [1, 5, 8]])
print("END\n")
print(a)
print(b)
