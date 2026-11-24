import operator
from collections import deque
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
        if self.conflict == "valid":
            return [self]
        if not self.children:
            return []

        return [leaf for c in self.children.values() for leaf in c.get_leaves()]

    @property
    def is_root(self) -> bool:
        return self.parent is None

    def parents_sets(self) -> set[frozenset]:
        addition = (
            {self.conflict} if self.conflict and self.conflict not in ("valid", "pruned") else set()
        )

        if self.is_root:
            return addition

        return addition | self.parent.parents_sets()


def pick_conflict(conflict_sets: set[frozenset]) -> frozenset:

    # MRV
    # Degree

    return list(conflict_sets)[0]


def score_conflict_candidates(node: Node, value: Any) -> tuple:
    score = []

    # LCV

    return tuple(score)


def label(node: Node) -> str:
    cn = sorted(node.conflict) if isinstance(node.conflict, frozenset) else node.conflict
    return f"HS: {sorted(node.hs)}, CN: {cn}"


def print_tree(node: Node, prefix: str = "", edge=None, last: bool = True):
    if edge is None:
        print(label(node))
        child_prefix = ""
    else:
        print(f"{prefix}{'└' if last else '├'}─{edge}─ {label(node)}")
        child_prefix = prefix + ("    " if last else "│   ")

    items = list(node.children.items())
    for i, (item, child) in enumerate(items):
        print_tree(child, child_prefix, item, i == len(items) - 1)


hit_tests, elem_ops = 0, 0


def get_evaluations():
    global hit_tests, elem_ops
    return hit_tests, elem_ops


def unhit_sets(hs: set, conflict_sets) -> list[frozenset]:
    global hit_tests, elem_ops

    out = []
    for cs in conflict_sets:
        # O(nR), n = |conflict_sets|, R = min size of smallest conflict set
        # https://theory.stanford.edu/~virgi/cs267/lecture5.pdf

        hit_tests += 1
        elem_ops += min(len(hs), len(cs))

        if hs.isdisjoint(cs):
            out.append(cs)
    return out


def find_min_hs(hitting_sets: list[set]) -> list[list]:
    minimal = []

    for hs in sorted(hitting_sets, key=len):
        if not any(min_hs.issubset(hs) for min_hs in minimal):
            minimal.append(hs)

    return [list(hs) for hs in minimal]


def run_hitting_set_algorithm(conflict_sets, **heuristics):
    """
    Algorithm that handles the entire process from conflict sets to hitting sets

    :param conflict_sets: list of conflict sets as list
    :return: the hitting sets and minimal hitting sets as list of lists
    """

    global hit_tests, elem_ops
    hit_tests, elem_ops = 0, 0

    # Empty conflict set, so no intersection possible.
    if any(len(cs) == 0 for cs in conflict_sets):
        return [], []

    conflict_sets = {frozenset(conflict) for conflict in conflict_sets}

    root = Node(set())
    queue = deque([root])
    hitting_sets = []

    while queue:
        node = queue.popleft()

        if heuristics.get("prune", False) and any(node.hs.issuperset(hs) for hs in hitting_sets):
            node.conflict = "pruned"
            continue

        unhit = unhit_sets(node.hs, conflict_sets - node.parents_sets())

        if not unhit:
            node.conflict = "valid"
            hitting_sets.append(node.hs)
            continue

        node.conflict = pick_conflict(unhit)

        for item in sorted(node.conflict, key=partial(score_conflict_candidates, node)):
            child = Node(node.hs | {item}, node)
            node.children[item] = child
            queue.append(child)

    # Seems like a waste to recollect if prune=True, but we need a line to typecast to lists anyway.
    hitting_sets = [list(l.hs) for l in root.get_leaves()]

    if heuristics.get("prune", False):
        min_hitting_sets = hitting_sets
    else:
        min_hitting_sets = find_min_hs([l.hs for l in root.get_leaves()])

    print_tree(root)

    return hitting_sets, min_hitting_sets


a, b = run_hitting_set_algorithm([[1, 2, 3], [3, 4, 5], [8, 5]], prune=True)
# print("END\n")
# print(a)
# print(b)
print(get_evaluations())

a, b = run_hitting_set_algorithm([[1, 2, 3], [3, 4, 5], [8, 5, 6, 99, 55]], prune=False)
print(get_evaluations())
