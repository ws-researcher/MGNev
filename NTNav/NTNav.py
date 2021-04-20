from RDFFile2Graph.Kg import KG
from queue import PriorityQueue
from KeywordSearch.NTNav.keywordMatch import *
import pandas as pd
import itertools as it
from functools import reduce
from datetime import *
import sys

class NTNav:

    def __init__(self, kg: KG, keywordList=None):
        if keywordList is None:
            keywordList = []
        self.kg = kg
        self.keywordList = keywordList

        path = './MetaGraphIndex.csv'
        self.Mindex, self.ontologyClass = self.reloadIndex(path)
        # self.ontologyClass = self.Mindex.index
        self.quDiagonalMindex = self.quDiagonal(self.Mindex)
        print("quDiagonalMindex" + str(sys.getsizeof(self.quDiagonalMindex)))

    def search(self):
        dt1 = datetime.now()
        answerList = []

        km = keywordMatch(self.kg, self.keywordList, self.ontologyClass)
        kgSearchNodeClassIdList, kgSearchNodeNameList = km.matchNTClass()
        kls = self.combine(kgSearchNodeClassIdList)
        for kl in kls:
            meatGraph = self.getTopMeatGraph(kl)
            self.comlete(meatGraph)
            answerGraph = self.navigate(meatGraph, kl)
            answerList.append(answerGraph)
        dt2 = datetime.now()
        dtc = dt2 - dt1
        print(dtc.microseconds)
        return sorted(answerList)


    def getTopMeatGraph(self, kgSearchNodeClassIdList):
        meatGraph = MeatGraph()
        restNodes = set()
        for s in kgSearchNodeClassIdList:
            if s.type == NodeType.attribution:
                pass
            else:
                restNodes.add(s.Class)

        visitedNode = set()
        while restNodes:
            if not visitedNode:
                singelIndex = self.quDiagonalMindex.loc[restNodes, restNodes]
                hangIndex, lieIndex = singelIndex.stack().idxmax()
                visitedNode.add(hangIndex)
                visitedNode.add(lieIndex)
                meatGraph.addMetaPath(self.Mindex[lieIndex][hangIndex])
                restNodes -= visitedNode
            else:
                singelIndex = self.quDiagonalMindex.loc[visitedNode, restNodes]
                hangIndex, lieIndex = singelIndex.stack().idxmax()
                visitedNode.add(hangIndex)
                visitedNode.add(lieIndex)
                meatGraph.addMetaPath(self.Mindex[lieIndex][hangIndex])
                restNodes -= visitedNode


        return meatGraph

    def navigate(self, meatGraph: MeatGraph, kl):
        typeId = self.kg.reversed_relations_id_dict.get('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
        mg = meatGraph.graph
        visitingClass = Stack()
        visitedClass = set()
        ceDict = dict()
        for k in kl:
            if k.nodeId is not None:
                visitingClass.push(k.Class)
                # kClassName = self.kg.entities_id_dict.get(k.Class)
                # knodeName = self.kg.entities_id_dict.get(k.nodeId)
                if k.Class in ceDict.keys():
                    ceDict[k.Class] = ceDict[k.Class] | {k.nodeId}
                else:
                    ceDict[k.Class] = {k.nodeId}
                # mg.add_relations({(k.nodeId, typeId, k.Class)})

        while not visitingClass.is_empty():
            vnode = visitingClass.pop()
            visitedClass.add(vnode)
            entityId = ceDict.get(vnode)
            if not entityId:
                continue
            rts = mg.rt_dict.get(vnode)
            if rts:
                for rt in rts:
                    r = rt[0]
                    c = rt[1]
                    T = Triple(vnode, r, c)
                    if T in visitedClass:
                        continue
                    else:
                        visitedClass.add(T)
                    # cname = self.kg.entities_id_dict.get(c)
                    tailNodes = ceDict.get(c, set())
                    visitingClass.push(c)
                    for head in entityId:
                        headname = self.kg.entities_id_dict.get(head)
                        rname = self.kg.relations_id_dict.get(r)
                        tailNodesName = self.kg.rev_hr_dict.get((headname, rname))
                        if tailNodes and tailNodesName:
                            tailNodes &= set(map(self.kg.reversed_entities_id_dict.get, tailNodesName))
                        elif not tailNodes and tailNodesName:
                            tailNodes = set(map(self.kg.reversed_entities_id_dict.get, tailNodesName))
                        else:
                            pass
                    ceDict[c] = tailNodes

            hrs = mg.hr_dict.get(vnode)
            if hrs:
                for hr in hrs:
                    r = hr[1]
                    c = hr[0]
                    T = Triple(vnode, r, c)
                    if T in visitedClass:
                        continue
                    else:
                        visitedClass.add(T)
                    # cname = self.kg.entities_id_dict.get(c)
                    headNodes = ceDict.get(c, set())
                    visitingClass.push(c)
                    for tail in entityId:
                        tailname = self.kg.entities_id_dict.get(tail)
                        rname = self.kg.relations_id_dict.get(r)
                        tailNodesName = self.kg.rev_hr_dict.get((tailname, rname))
                        if headNodes and tailNodesName:
                            headNodes &= set(map(self.kg.reversed_entities_id_dict.get, tailNodesName))
                        elif not headNodes and tailNodesName:
                            headNodes = set(map(self.kg.reversed_entities_id_dict.get, tailNodesName))
                        else:
                            pass
                    ceDict[c] = headNodes

        nodeList = set()
        for k in ceDict.keys():
            nodeList.add(k)
            nodeList |= ceDict.get(k)
            # for n in ceDict.get(k):
            #     mg.add_relations({(n, typeId, k)})
        answerGraph = self.kg.getSubgraph(nodeList)
        return answerGraph

    def isGraph(self, nodeList=None):
        if nodeList is None:
            nodeList = []

        initNode = nodeList[0]
        lastNodeSet = {initNode}
        remainNodeSet = set(nodeList) - lastNodeSet

        while remainNodeSet:
            neighborNodeSet = {}
            for node in lastNodeSet:
                neighborsSet = self.kg.NBR(node)
                neighborNodeSet |= neighborsSet

            lastNodeSet = remainNodeSet & neighborNodeSet
            if not lastNodeSet:
                return False

            remainNodeSet = remainNodeSet - neighborNodeSet

        return True

    def reloadIndex(self, filePath):
        matePathIndex = pd.read_csv(filePath, index_col=[0])
        ontologyClass = list(matePathIndex.index)
        matePathIndex = matePathIndex.applymap(self.name2id)
        matePathIndex.index = matePathIndex.index.map(lambda x: self.kg.reversed_entities_id_dict.get(x) if x in self.kg.reversed_entities_id_dict.keys() else self.kg.reversed_relations_id_dict.get(x))
        matePathIndex.columns = matePathIndex.columns.map(lambda y: self.kg.reversed_entities_id_dict.get(y) if y in self.kg.reversed_entities_id_dict.keys() else self.kg.reversed_relations_id_dict.get(y))
        return matePathIndex, ontologyClass

    def name2id(self, x):
        if isinstance(x, str):
            tGraphSet = set()
            x = eval(x)
            if x:
                for tpath in x:
                    tGraph = MeatGraph()
                    for path in tpath[0]:
                        path = eval(path)
                        metaPath = MetaPath()
                        for i in range(len(path)):
                            if i % 2 == 0:
                                entityName = path[i]
                                id = self.kg.reversed_entities_id_dict.get(entityName)
                                path[i] = IdClassType(None, id, NodeType.entity)
                                metaPath.addNode(path[i])
                            else:
                                relationName = path[i][0]
                                prob = path[i][1]
                                id = self.kg.reversed_relations_id_dict.get(relationName)
                                path[i] = IdClassType(None, id, NodeType.relation, prob=prob)
                                metaPath.addNode(path[i])
                        tGraph.addMetaPath(metaPath)
                    tGraph.score = tpath[1]
                    tGraphSet.add(tGraph)
                return max(tGraphSet)
            else:
                return set()


    def quDiagonal(self, Mindex):
        Mindex = Mindex.applymap(lambda x: x.score if isinstance(x, MeatGraph) else 0)
        # print(Mindex)
        length = len(Mindex)
        for i in range(length):
            Mindex.iloc[i,i] =0
        return Mindex

    #item: [{},{},{}]
    def combine(self, item):
        res = []
        for s in item:
            tem = []
            for x in s:
                tem.append([x])
            res.append(tem)
        combine = reduce(self.combination, res)
        return combine


    def combination(self,dict1,dict2):
        ele = []
        for ele1 in dict1:
            for ele2 in dict2:
                ele.append(ele1 + ele2)
        return ele

    def comlete(self, meatGraph):
        mg = meatGraph.graph
        cList = mg.entities_list
        self.kg.getEntitySubgraph(cList, mg)
