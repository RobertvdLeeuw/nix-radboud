class Node:
    # Node in the hitting set tree. Each node has a set of components that have been chosen to be in the hitting set, and a list of conflict sets that have not yet been hit.

    def __init__(self, path, parent=None):
        self.path = path
        self.parent = parent
        self.children = []
        self.label = None
        self.complete = False
        self.pruned = False


# Helper functions
def getUnhitSets(conflictSets, path):
    return [cs for cs in conflictSets if not (cs & path)]


def containsKnownHittingSet(path, hittingSets):
    for hittingSet in hittingSets:
        if hittingSet.issubset(path):
            return True
    return False


def runHittingSetAlgorithm(conflictSets):
    """
    Algorithm that handles the entire process from conflict sets to hitting sets

    :param conflict_sets: list of conflict sets as list
    :return: the hitting sets and minimal hitting sets as list of lists
    """
    sets = []
    for conflictSet in conflictSets:
        sets.append(set(conflictSet))

    for conflictSet in sets:
        if len(conflictSet) == 0:
            return [], []

    hittingSets = []

    root = Node(set())
    openNodes = [root]
    seenSets = []

    while len(openNodes) > 0:
        activeNode = openNodes.pop()

        if containsKnownHittingSet(activeNode.path, hittingSets):
            activeNode.pruned = True
            continue

        unhit = getUnhitSets(sets, activeNode.path)

        if len(unhit) == 0:
            activeNode.complete = True
            hittingSets.append(activeNode.path)
            continue

        activeSet = unhit[0]
        activeNode.label = activeSet

        for component in sorted(activeSet):
            newPath = activeNode.path | {component}

            if newPath in seenSets:
                continue
            seenSets.append(newPath)
            child = Node(newPath, parent=activeNode)
            activeNode.children.append(child)
            openNodes.append(child)

    minimalHittingSets = []
    for hittingSet in hittingSets:
        if not any(other < hittingSet for other in hittingSets):
            minimalHittingSets.append(hittingSet)

    return (
        [sorted(hs) for hs in hittingSets],
        [sorted(hs) for hs in minimalHittingSets],
    )
