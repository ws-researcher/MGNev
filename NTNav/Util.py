from enum import Enum
from KeywordSearch.NTNav.Exceptions import *
from RDFFile2Graph.Kg import KG

class MeatGraph(object):
    def __init__(self):
        self.__score = 0
        self.__metaPaths = []
        self.__graph = KG()
        self.__Aconstraint = set()

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score > other.score

    def __le__(self, other):
        return self.score <= other.score

    def __hash__(self):
        return hash(self.__score)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__score == other.score
        else:
            return False

    @property
    def metaPaths(self):
        return self.__metaPaths


    @property
    def graph(self):
        return self.__graph

    def addMetaPath(self, metaPath):
        if isinstance(metaPath, MetaPath):
            self.__metaPaths.append(metaPath)
            self.score = self.merge(self.__metaPaths)
        elif isinstance(metaPath, MeatGraph):
            for path in metaPath.metaPaths:
                self.__metaPaths.append(path)
            self.score = self.merge(self.__metaPaths)
        else:
            print('It is not a MeatGraph/MetaPath object')

    def merge(self, paths):
        allP = set()
        for p in paths:
            allP |= set(path2Triples(p))
            if len(p) > 1:
                for t in set(path2Triples(p)):
                    self.__graph.add_relations({(t.head.Class, t.relation.Class, t.tail.Class)})

        pathProb = 1
        for T in allP:
            pathProb *= T.prob

        return pathProb

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        self.__score = score

    @property
    def Aconstraint(self):
        return self.__Aconstraint

    # cst: (entity, attribution, value)
    def addAconstraint(self, cst: tuple):
        self.__Aconstraint.add(cst)



class NodeType(Enum):
    entity = 1
    relation = 2
    attribution = 3
    # value = 4


class IdClassType(object):

    def __init__(self, nodeId, Class, type: NodeType, prob=None):
        self.__nodeId = nodeId
        self.__Class = Class
        # entity, relation
        self.__type = type
        self.__prob = prob  # prob of relation

    def __hash__(self):
        return hash((self.__nodeId, self.__Class, self.__type))

    @property
    def prob(self):
        return self.__prob

    @property
    def nodeId(self):
        return self.__nodeId

    @nodeId.setter
    def nodeId(self, value):
        if isinstance(value, str):
            self.__nodeId = value
        else:
            print("error：The input type is inconsistent with the preset type")

    @property
    def Class(self):
        return self.__Class

    @Class.setter
    def Class(self, value):
        if isinstance(value, str):
            self.__Class = value
        else:
            print("error：The input type is inconsistent with the preset type")

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if isinstance(value, str):
            self.__type = value
        else:
            print("error：The input type is inconsistent with the preset type")


class MetaPath(object):

    def __init__(self):
        # self.__rt = None
        self.__path = []
        self.__prob = None

    def __len__(self):
        return len(self.__path)

    def __lt__(self, other):
        return self.prob < other.prob

    def __gt__(self, other):
        return self.prob > other.prob

    def __getitem__(self, item):
        return self.__path[item]


    @property
    def prob(self):
        return self.__prob

    @prob.setter
    def prob(self, value):
        if isinstance(value, float):
            self.__prob = value
        else:
            print("error：The input type is inconsistent with the preset type")

    @property
    def path(self):
        return self.__path

    def addNode(self, node: IdClassType):

        if (len(self) % 2) == 0 and node.type == NodeType.entity:
            self.__path.append(node)
        elif (len(self) % 2) == 0 and node.type != NodeType.entity:
            raise NodeError('The node whit even index should be a Entity instead of {}'.format(node.type))
        elif (len(self) % 2) == 1 and node.type == NodeType.relation:
            self.__path.append(node)
        else:
            raise NodeError('The node whit odd index should be a Relation instead of {}'.format(node.type))


class Stack(object):

    def __init__(self):
        self.__list = []

    def __len__(self):
        return len(self.__list)

    def __iter__(self):
        return iter(self.__list)

    def __str__(self):
        return str(self.__list)

    def is_empty(self):
        return self.__list == []

    def push(self, item):
        self.__list.append(item)

    def pop(self):
        if self.is_empty():
            return
        else:
            return self.__list.pop()

    def top(self):
        if self.is_empty():
            return
        else:
            return self.__list[-1]

    def toList(self):
        return self.__list

    def toSet(self):
        return set(self.__list)

    def __getitem__(self, index):
        if self.is_empty():
            return
        else:
            return self.__list[index]

    def index(self, item):
        return self.__list.index(item)

class Triple(object):
    def __init__(self, head, relation, tail, prob=None):
        self.__head = head
        self.__relation = relation
        self.__tail = tail
        self.__prob = prob

    @property
    def head(self):
        return self.__head

    @property
    def relation(self):
        return self.__relation

    @property
    def tail(self):
        return self.__tail

    @property
    def prob(self):
        return self.__prob

    def __hash__(self):
        return hash((self.__head, self.__relation, self.__tail))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        else:
            return False


def twoPathProb(path1: str, path2: str):
    path1TripleList = path2Triples(path1)
    path2TripleList = path2Triples(path2)
    if path1TripleList is None or path2TripleList is None:
        print('s')

    pathTripleSet = set(path1TripleList) | set(path2TripleList)
    pathProb = 1
    for T in pathTripleSet:
        pathProb *= T.prob
    return pathProb


def path2Triples(path):
    if isinstance(path, list):
        lenpath = len(path)
        pathTripleList = []
        if lenpath == 1:
            pathTripleList = [Triple(path[0], None, None, 1)]
        else:
            for i in range(lenpath):
                if i % 2 == 0 and i != 0:
                    pathTripleList.append(Triple(path[i - 2], path[i - 1][0], path[i], path[i - 1][1]))
        return pathTripleList
    elif isinstance(path, MetaPath):
        lenpath = len(path)
        pathTripleList = []
        if lenpath == 1:
            pathTripleList = [Triple(path[0], None, None, 1)]
        else:
            for i in range(lenpath):
                if i % 2 == 0 and i != 0:
                    pathTripleList.append(Triple(path[i - 2], path[i - 1], path[i], path[i - 1].prob))
        return pathTripleList
