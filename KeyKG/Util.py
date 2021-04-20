def findMinPathNode(df, id, U):
    distSet = set()
    for u in U:
        # print(df[id])
        vHopDict = df[id]
        uHopDict = df[u]
        intersection = set(vHopDict.keys()) & set(uHopDict.keys())
        if len(intersection) == 0:
            minDistNode = HLHop(float('inf'), id)
            distSet.add(minDistNode)
        else:
            for iNode in intersection:
                vOneHop = vHopDict[iNode]
                uOneHop = uHopDict[iNode]
                hop = HLHop(vOneHop.dist + uOneHop.dist, iNode)
                distSet.add(hop)

    minDistNode = min(distSet)
    return minDistNode


class HLHop:

    def __init__(self, dist=None, pred=None):
        self.dist = dist
        self.pred = pred

    def __lt__(self, other):
        return self.dist < other.dist

    def __gt__(self, other):
        return self.dist > other.dist
