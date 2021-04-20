from RDFFile2Graph.Kg import KG
from RDFFile2Graph.ReadRDFFile import ReadRDFFile
import pandas as pd
import csv
from KeywordSearch.NTNav.Util import *
import math


class CreatMetaGraphIndex:

    def __init__(self, networkSchema: KG):
        self.__networkSchema = networkSchema

    def meatPathStack2list(self, meatPath: Stack):
        path = []
        for item in meatPath:
            if item.relation is not None:
                path.append(item.relation)
            if item.itself is not None:
                path.append(item.itself)

        return str(path)

    def creatMeatGraphIndex(self):

        entityList = self.__networkSchema.entities_list
        matGraphIndex = pd.DataFrame(index=entityList, columns=entityList)
        matGraphIndex = matGraphIndex.applymap(lambda x: set() if math.isnan(x) else x)
        for entity in entityList:
            visited = set()
            visiteNode = Stack()
            meatPath = Stack()

            visiteNode.push(MeatPathNode(None, None, entity, 1))

            while not visiteNode.is_empty():
                if not meatPath.is_empty():
                    TailNode = meatPath.top()
                    childNode = self.__networkSchema.rt_dict.get(TailNode.itself, set())
                    childNodeSet = {MeatPathNode(TailNode.itself, x[0], x[1], None) for x in childNode}

                    while not childNode or childNodeSet.issubset(visited):
                        meatPath.pop()
                        if not meatPath.is_empty():
                            TailNode = meatPath.top()
                            childNode = self.__networkSchema.rt_dict.get(TailNode.itself, set())
                            childNodeSet = {MeatPathNode(TailNode.itself, x[0], x[1], None) for x in childNode}
                        else:
                            break

                nextNode = visiteNode.pop()
                visited.add(nextNode)
                meatPath.push(nextNode)

                last = matGraphIndex[nextNode.itself][entity]
                if not last:
                    matGraphIndex[nextNode.itself][entity] = {(self.meatPathStack2list(meatPath), nextNode.prob)}
                elif isinstance(last, set):
                    last.add((self.meatPathStack2list(meatPath), nextNode.prob))
                else:
                    print('s')

                tList = self.__networkSchema.rt_dict.get(nextNode.itself, set())
                clildNum = len(tList)
                for child in tList:
                    childPathNode = MeatPathNode(nextNode.itself, child[0], child[1], nextNode.prob / clildNum)
                    if childPathNode not in visited and child[1] != entity:
                        visiteNode.push(childPathNode)



        matGraphIndex.to_csv("MetaGraphIndex.csv", sep=',', header=True, index=True)


class MeatPathNode(object):
    def __init__(self, parents, relation, itself, prob):
        self.__parents = parents
        self.__relation = relation
        self.__itself = itself
        self.__prob = prob

    @property
    def parents(self):
        return self.__parents

    @property
    def relation(self):
        return self.__relation

    @property
    def itself(self):
        return self.__itself

    @property
    def prob(self):
        return self.__prob

    def __hash__(self):
        return hash((self.__parents, self.__relation, self.__itself))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__parents == other.parents and self.__relation == other.relation and self.__itself == other.itself
        else:
            return False

    def __mul__(self, other):
        self.__prob *= other.prob


# r = ReadRDFFile("../../dataSet/CTIO.nt")
# kg = r.file2graph()
#
# c = CreatMetaGraphIndex(kg)
# c.creatMeatGraphIndex()
