# coding=utf-8
import pandas as pd
import csv
from KeywordSearch.NTNav.Util import *
import math
import copy
from RDFFile2Graph.GraphPrecessing import GraphPrecessing
from collections import deque

from RDFFile2Graph.ReadRDFFile import ReadRDFFile


class CreatMeatGraphIndex:

    def __init__(self, networkSchema: KG):
        self.__networkSchema = networkSchema

    def meatPathStack2list(self, meatPath: Stack):
        copyMetapath = deque(meatPath.toList())
        path = []
        item1 = copyMetapath.popleft()
        path.append(item1.itself)
        while copyMetapath:
            item = copyMetapath.popleft()
            if item.relation == 'rdf-schema#subClassOf' and len(path) == 1 and not copyMetapath:
                return None
            # elif item.relation == 'rdf-schema#subClassOf' and len(path) == 1 and copyMetapath:
            #     continue
            elif item.relation == 'rdf-schema#subClassOf' and copyMetapath:
                continue
            elif item.relation == 'rdf-schema#subClassOf' and len(path) > 1 and not copyMetapath:
                del(path[-1])
                path.append(item.itself)
            else:
                path.append((item.relation, item.prob))
                path.append(item.itself)


            # if item.relation is not None:
            #     if item.relation == 'rdf-schema#subClassOf' and meatPath.index(item) == length - 1:
            #         tem = path[-1]
            #         path.remove(tem)
            #     else:
            #         path.append((item.relation, item.prob))
            # if item.itself is not None:
            #     path.append(item.itself)

        return path

    def creatMeatGraphIndex(self, savePath=''):
        entityList = self.__networkSchema.entities_list
        relationList = self.__networkSchema.relations_list
        if 'rdf-schema#subClassOf' in relationList:
            relationList.remove('rdf-schema#subClassOf')
        with open(savePath + "pathIndex.csv", "w", encoding='utf-8') as MeatGraphIndex:
            writer = csv.writer(MeatGraphIndex)
            writer.writerow(["root", "tail", "path", "prob"])

            for entity in entityList:
                if entity == 'Taxon':
                    print('s')
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

                    prob = 1
                    for n in meatPath:
                        prob *= n.prob

                    meatPathList = self.meatPathStack2list(meatPath)
                    if isinstance(meatPathList, list):
                        writer.writerow([entity, nextNode.itself, meatPathList, prob])
                        length = len(meatPathList)
                        if length >= 2:
                            relation = meatPathList[-2]
                            meatPathList[-2] = [relation[0], 1.0]
                            rprob = 1
                            l = list(range(length))
                            for i in l[1::2]:
                                relationi = meatPathList[i]
                                rprob *= relationi[1]
                            writer.writerow([entity, relation[0], meatPathList, rprob])

                    # if len(meatPath) >= 2:
                    #     copyMetapath = copy.deepcopy(meatPath)
                    #     a = copyMetapath[-1]
                    #     copyMetapath[-1].prob = 1.00
                    #     rprob = 1
                    #     for i in range(len(copyMetapath)):
                    #         rprob *= copyMetapath[i].prob
                    #     writer.writerow([entity, nextNode.relation, self.meatPathStack2list(copyMetapath), rprob])

                    tList = self.__networkSchema.rt_dict.get(nextNode.itself, set())
                    clildNum = len(tList)
                    for child in tList:
                        childPathNode = MeatPathNode(nextNode.itself, child[0], child[1], nextNode.prob / clildNum)
                        # if childPathNode not in visited and child[1] != entity:
                        if childPathNode not in visited:
                            visiteNode.push(childPathNode)

        path = savePath + 'pathIndex.csv'
        matePathIndex1 = pd.read_csv(path, index_col=['root', 'tail'])
        matePathIndex2 = pd.read_csv(path, index_col=['tail', 'root'])
        matePathIndex1['path'] = matePathIndex1['path'].map(eval)
        matePathIndex2['path'] = matePathIndex2['path'].map(eval)

        index = entityList + relationList
        matGraphIndex = pd.DataFrame(index=index, columns=index)
        matGraphIndex = matGraphIndex.applymap(lambda x: set() if math.isnan(x) else x)

        matePathIndex1.sort_index()
        matePathIndex2.sort_index()
        matGraphIndex.sort_index()

        for entity1 in entityList:
            print(entity1)
            for entity2 in entityList:
                Ofid1 = set(matePathIndex1.loc[entity1].index) | set(matePathIndex2.loc[entity1].index)
                Ofid2 = set(matePathIndex1.loc[entity2].index) | set(matePathIndex2.loc[entity2].index)
                roots = Ofid1 & Ofid2
                maxPath = set()
                probinit = 0
                for root in roots:
                    path1, prob1 = self.getTwoidPath(root, entity1, matePathIndex1)
                    path2, prob2 = self.getTwoidPath(root, entity2, matePathIndex1)
                    prob = twoPathProb(path1, path2)
                    if prob >= probinit:
                        probinit = prob
                        maxPath.add(((str(path1), str(path2)), prob))

                matGraphIndex[entity1][entity2] |= maxPath

        for relation in relationList:
            b = matePathIndex2.loc[relation]
            for entityx in set(b.index):
                paths = set()
                rpath, prob = self.getTwoidPath(relation, entityx, matePathIndex2)
                paths.add(((str(rpath), str(rpath)), prob))
                matGraphIndex[entityx][relation] |= paths
                matGraphIndex[relation][entityx] |= paths

        matGraphIndex.to_csv(savePath + "MetaGraphIndex.csv", sep=',', header=True, index=True)

    def getTwoidPath(self, root, id, matePathIndex):
        path = None
        pp = 0
        if (root, id) in matePathIndex.index:
            metaPath = matePathIndex.loc[root].loc[id]
            if isinstance(metaPath, pd.DataFrame):
                for i in range(len(metaPath)):
                    metaPathi = metaPath.iloc[i].loc['path']
                    pathProbi = metaPath.iloc[i].loc['prob']
                    if pathProbi >= pp:
                        pp = pathProbi
                        path = metaPathi
            else:
                metaPathi = metaPath.loc['path']
                pathProbi = metaPath.loc['prob']
                if pathProbi >= pp:
                    pp = pathProbi
                    path = metaPathi

        if (id, root) in matePathIndex.index:
            metaPath = matePathIndex.loc[id].loc[root]
            if isinstance(metaPath, pd.DataFrame):
                for i in range(len(metaPath)):
                    metaPathi = metaPath.iloc[i].loc['path']
                    pathProbi = metaPath.iloc[i].loc['prob']
                    if pathProbi >= pp:
                        pp = pathProbi
                        path = metaPathi
            else:
                metaPathi = metaPath.loc['path']
                pathProbi = metaPath.loc['prob']
                if pathProbi >= pp:
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

    @parents.setter
    def parents(self, value):
        if isinstance(value, str):
            self.__parents = value
        else:
            print("error：The input type is inconsistent with the preset type")

    @property
    def relation(self):
        return self.__relation

    @relation.setter
    def relation(self, value):
        if isinstance(value, str):
            self.__relation = value
        else:
            print("error：The input type is inconsistent with the preset type")

    @property
    def itself(self):
        return self.__itself

    @itself.setter
    def itself(self, value):
        if isinstance(value, str):
            self.__itself = value
        else:
            print("error：The input type is inconsistent with the preset type")

    @property
    def prob(self):
        return self.__prob

    @prob.setter
    def prob(self, value):
        if isinstance(value, float):
            self.__prob = value
        else:
            print("error：The input type is inconsistent with the preset type")

    def __hash__(self):
        return hash((self.__parents, self.__relation, self.__itself))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__parents == other.parents and self.__relation == other.relation and self.__itself == other.itself
        else:
            return False

    def __mul__(self, other):
        self.__prob *= other.prob


kg = KG()
r = ReadRDFFile()
r.file2graph(kg, "D:/ws/aa/KeywordSearch/dataSet/CTIKG/CTIKGO.nt")

c = CreatMeatGraphIndex(kg)
c.creatMeatGraphIndex('')

# kg = KG()
# r = GraphPrecessing(kg)
# r.ontologyPrecess('D:/workplace/python/KeywordSearch/dataSet/Yago4/yago-wd-schema.nt')
# c = CreatMeatGraphIndex(kg)
# c.creatMeatGraphIndex('D:/')


