from RDFFile2Graph.Kg import KG
from RDFFile2Graph.ReadRDFFile import ReadRDFFile
import pandas as pd
import csv
from KeywordSearch.NTNav.Util import *
import math

class CreatMeatGraphIndex:

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
        relationList = self.__networkSchema.relations_list
        with open("pathIndex.csv", "w") as MeatGraphIndex:
            writer = csv.writer(MeatGraphIndex)
            writer.writerow(["root", "tail", "path", "prob"])

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
                    writer.writerow([entity, nextNode.itself, self.meatPathStack2list(meatPath), nextNode.prob])



                    tList = self.__networkSchema.rt_dict.get(nextNode.itself, set())
                    clildNum = len(tList)
                    for child in tList:
                        childPathNode = MeatPathNode(nextNode.itself, child[0], child[1], nextNode.prob / clildNum)
                        if childPathNode not in visited and child[1] != entity:
                            visiteNode.push(childPathNode)


        path = './pathIndex.csv'
        matePathIndex1 = pd.read_csv(path, index_col=['root', 'tail'])
        matePathIndex2 = pd.read_csv(path, index_col=['tail', 'root'])
        matePathIndex1['path'] = matePathIndex1['path'].map(eval)
        matePathIndex2['path'] = matePathIndex2['path'].map(eval)

        matGraphIndex = pd.DataFrame(index=entityList, columns=entityList)
        matGraphIndex = matGraphIndex.applymap(lambda x: set() if math.isnan(x) else x)

        for entity1 in entityList:
            for entity2 in entityList:
                Ofid1 = set(matePathIndex1.loc[entity1].index) | set(matePathIndex2.loc[entity1].index)
                Ofid2 = set(matePathIndex1.loc[entity2].index) | set(matePathIndex2.loc[entity2].index)
                roots = Ofid1 & Ofid2
                maxPath = set()
                for root in roots:
                    path1, prob1 = self.getTwoidPath(root, entity1, matePathIndex1)
                    path2, prob2 = self.getTwoidPath(root, entity2, matePathIndex1)
                    maxPath.add(((str(path1), str(path2)), prob1*prob2))

                matGraphIndex[entity1][entity2] |= maxPath

        matGraphIndex.to_csv("MetaGraphIndex.csv", sep=',', header=True, index=True)

    def getTwoidPath(self,root, id, matePathIndex):
        path = None
        pp = 0
        if (root, id) in matePathIndex.index:
            metaPath = matePathIndex.loc[root].loc[id]
            if isinstance(metaPath, pd.DataFrame):
                for i in range(len(metaPath)):
                    metaPathi = metaPath.iloc[i].loc['path']
                    pathProbi = metaPath.iloc[i].loc['prob']
                    if pathProbi > pp:
                        pp = pathProbi
                        path = metaPathi
            else:
                metaPathi = metaPath.loc['path']
                pathProbi = metaPath.loc['prob']
                if pathProbi > pp:
                    pp = pathProbi
                    path = metaPathi

        if (id, root) in matePathIndex.index:
            metaPath = matePathIndex.loc[id].loc[root]
            if isinstance(metaPath, pd.DataFrame):
                for i in range(len(metaPath)):
                    metaPathi = metaPath.iloc[i].loc['path']
                    pathProbi = metaPath.iloc[i].loc['prob']
                    if pathProbi > pp:
                        pp = pathProbi
                        path = metaPathi
            else:
                metaPathi = metaPath.loc['path']
                pathProbi = metaPath.loc['prob']
                if pathProbi > pp:
                    pp = pathProbi
                    path = metaPathi

        return path, pp


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
# c = CreatMeatGraphIndex(kg)
# c.creatMeatGraphIndex()
