import operator
from functools import partial, reduce
from itertools import combinations
from typing import Self


class Node:
    def __init__(self, hs: set, parent: Self | None = None):
        self.hs: set = hs
        self.conflict: frozenset = None

        self.parent = parent
        self.children = dict()

    def get_leaves(self) -> list:
        if self.conflict == "terminal":
            return [self]
        if not self.children:
            return []

        return [leaf for c in self.children.values() for leaf in c.get_leaves()]

    @property
    def is_root(self) -> bool:
        return self.parent is None

    def checked_sets(self) -> set[frozenset]:
        addition = {self.conflict} if self.conflict and self.conflict != "terminal" else set()

        if self.is_root:
            return addition

        return addition | self.parent.checked_sets()

    @property
    def root(self) -> Self:
        return self if self.is_root else self.parent.root

    @property
    def n(self) -> int:
        return 1 if self.is_leaf else sum(c.n for c in self.children)

    @property
    def abs_depth(self) -> int:
        return 0 if self.is_root else self.parent.abs_depth + 1


def pick_conflict(conflict_sets: set[frozenset]) -> frozenset:
    return list(conflict_sets)[0]


def run_hitting_set_algorithm(conflict_sets):
    """
    Algorithm that handles the entire process from conflict sets to hitting sets

    :param conflict_sets: list of conflict sets as list
    :return: the hitting sets and minimal hitting sets as list of lists
    """

    conflict_sets = {frozenset(conflict) for conflict in conflict_sets}

    def process(node: Node):
        for item in sorted(node.conflict):
            child = Node(node.hs | {item}, node)
            node.children[item] = child
            stack.append(child)

    root = Node(set())
    stack = [root]

    while stack:
        node = stack.pop()  # TODO: stack or queue?

        unhit = list(
            filter(lambda cs: not node.hs.intersection(cs), conflict_sets - node.checked_sets())
        )

        if not unhit:
            node.conflict = "terminal"
            continue

        node.conflict = pick_conflict(unhit)

        process(node)

    hitting_sets = [list(l.hs) for l in root.get_leaves()]
    from pprint import pprint

    pprint(hitting_sets)

    return hitting_sets, min_hitting_sets


a, b = run_hitting_set_algorithm([[1, 2, 3], [3, 4, 5], [8, 5]])
print("END\n")
print(a)
print(b)
