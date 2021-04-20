
class AnswerTree(object):

    def __init__(self):
        self.edges = set()
        self.nodes = set()
        self.score = 0

    def __lt__(self, other):
        return self.score > other.score


    def addPath(self,kg, path : list):
        lengthOfPath = len(path)

        path = list(map(lambda x: kg.entities_id_dict.get(x), path))

        self.nodes |= set(path)
        for i in range(lengthOfPath):
            if i <= lengthOfPath - 2:
                edge = (path[i], path[i+1])
                self.edges.add(edge)
