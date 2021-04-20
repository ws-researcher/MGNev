from queue import PriorityQueue
from KeywordSearch.BanksII.MaxHeap import *
from KeywordSearch.Util.AnswerTree import *
import numpy as np
import pandas as pd

from KeywordSearch.Util.keywordMatch import keywordMatch
from datetime import *

class BanksT:

    def __init__(self, kg, keywordList = []):
        self.kg = kg
        self.keywordList = keywordList

        self.dmax = 8
        self.mu = 0.5

        # 节点信誉度，此处默认所有节点信誉度为1
        self.prestige = 1
        # 单边距离/权重
        self.wight = 1

        # self.nodeNum = self.kg.entities_num + self.kg.relations_num + self.kg.attributes_num
        self.nodeNum = self.kg.entities_num
        self.keywordNum = len(self.keywordList)

        self.Qin = MaxHeap()
        self.Qout = MaxHeap()

        self.Xin = set()
        self.Xout = set()

        km = keywordMatch(kg, self.keywordList)
        self.kgSearchNodeIdList, self.kgSearchNodeNameList = km.kwMatch()

        entitiesIds = self.kg.entities_id_dict.keys()

        self.sp = pd.DataFrame(index=entitiesIds, columns=range(self.keywordNum))


        #存储路径长度
        d = np.zeros((self.nodeNum, self.keywordNum)) - 1
        self.dist = pd.DataFrame(d, index=entitiesIds, columns=range(self.keywordNum))

        aa = np.zeros((self.nodeNum, self.keywordNum))
        self.act = pd.DataFrame(aa, index=entitiesIds, columns=range(self.keywordNum))

        a = np.zeros((self.nodeNum,1))
        self.activation = pd.DataFrame(a, index=entitiesIds, columns=range(1))

        #存储遍历层数
        dp = np.zeros((self.nodeNum, 1)) - 1
        self.depth = pd.DataFrame(dp, index=entitiesIds, columns=range(1))

        for i in range(self.keywordNum):
            Si = self.kgSearchNodeIdList[i]
            for id in Si:
                self.dist[i][id] = 0
                act = self.prestige/len(Si)
                self.act[i][id] = act
                self.sp[i][id] = id
                self.activation[0][id] += self.act[i][id]
                self.depth[0][id] = 0
                self.Qin.pushAndChange(HeapNode(id, self.activation[0][id]))


        self.answerQueue = PriorityQueue()

# 主题方法
    def search(self):
        dt1 = datetime.now()
        while not self.Qin.isEmpty() or not self.Qout.isEmpty():
            maxact = -1
            bOrf = -1
            if not self.Qin.isEmpty():
                topNodeIn = self.Qin.getTop()
                if topNodeIn.activation > maxact:
                    maxact = topNodeIn.activation
                    bOrf = 0

            if not self.Qout.isEmpty():
                topNodeOut = self.Qout.getTop()
                if topNodeOut.activation > maxact:
                    maxact = topNodeOut.activation
                    bOrf = 1

            if maxact == -1:
                break

            self.extend(bOrf)
        dt2 = datetime.now()
        dtc = dt2 - dt1
        print(dtc.microseconds)
        return self.answerQueue



    def extend(self, bOrf : bool):

        if bOrf == 0:
            bestNode = self.Qin.pop()
            id = bestNode.id
            self.Xin.add(id)
            if self.isComplete(id):
                self.emit(id)
            if self.depth[0][id] < self.dmax:
                nodeName = self.kg.entities_id_dict.get(id)
                incomingNode = self.kg.hr_dict.get(nodeName)
                if incomingNode is None: return
                nodeSetSize = len(incomingNode)
                for rnode in incomingNode:
                    expNodeName = rnode[0]
                    expNodeId = self.kg.reversed_entities_id_dict.get(expNodeName)
                    if expNodeId is not None:
                        self.ExploreEdge(expNodeId, id, nodeSetSize)
                    if expNodeId not in self.Xin and expNodeId not in self.Xout:
                        self.Qin.pushAndChange(HeapNode(expNodeId, self.activation[0][expNodeId]))
                        self.depth[0][expNodeId] = self.depth[0][id] + 1
                    if id not in self.Xout:
                        self.Qout.pushAndChange(HeapNode(id, self.activation[0][id]))

        if bOrf == 1:
            bestNode = self.Qout.pop()
            id = bestNode.id
            self.Xout.add(id)
            if self.isComplete(id):
                self.emit(id)
            if self.depth[0][id] < self.dmax:
                nodeName = self.kg.entities_id_dict.get(id)
                outcomingNode = self.kg.rt_dict.get(nodeName)
                if outcomingNode is None: return
                outnodeSetSize = len(outcomingNode)
            for node in outcomingNode:
                expNodeNmae = node[0]
                expNodeId = self.kg.reversed_entities_id_dict.get(expNodeNmae)
                if expNodeId is not None:
                    self.ExploreEdge(id, expNodeId, outnodeSetSize)

                if id not in self.Xout:
                    self.Qout.pushAndChange(HeapNode(id, self.activation[0][id]))
                    self.depth[0][id] = self.depth[0][expNodeId] + 1
        else:
            pass


    def isComplete(self, id):
        dl = list(self.dist.loc[id])
        return -1 not in dl

    def emit(self, id):
        answerTree = AnswerTree()
        for i in range(self.keywordNum):
            path = list()
            path.append(id)
            lastId = id
            while True:
                nextId = self.sp[i][lastId]
                if nextId != lastId:
                    path.append(nextId)
                    lastId = nextId
                else:
                    break
            answerTree.addPath(self.kg, path)

        answerTree.score = len(answerTree.edges)
        self.answerQueue.put(answerTree)



    def ExploreEdge(self, expNodeId, id, nodeSetSize):

        for i in range(self.keywordNum):
            #路径越短越好
            if self.dist[i][id] >= 0 and (self.dist[i][expNodeId] < 0 or self.dist[i][expNodeId] > self.dist[i][id] + self.wight):
                self.sp[i][expNodeId] = id
                self.dist[i][expNodeId] = self.dist[i][id] + self.wight
                self.Attach(expNodeId, i)
                if self.isComplete(expNodeId):
                    # name = self.kg.entities_id_dict.get(expNodeId)
                    # print(name)
                    # name = self.kg.entities_id_dict.get(id)
                    # print(name)
                    self.emit(expNodeId)

            at = (1 - self.mu) * self.act[i][id] / nodeSetSize
            if self.act[i][expNodeId] < at:
                self.act[i][expNodeId] = at
                self.Activate(expNodeId, i, nodeSetSize)


    def Attach(self, expNodeId, i):
        # if expNodeId in self.Qin.idIndex.keys():
        nodeName = self.kg.entities_id_dict.get(expNodeId)
        ancestors = self.kg.hr_dict.get(nodeName)
        if ancestors is None:
            return
        for node in ancestors:
            nextExpNodeNmae = node[0]
            nextExpNodeId = self.kg.reversed_entities_id_dict.get(nextExpNodeNmae)
            if self.dist[i][nextExpNodeId] >= 0:
                self.dist[i][nextExpNodeId] = self.dist[i][expNodeId] + self.wight

    def Activate(self, expNodeId, i, nodeSetSiza):

        # if expNodeId in self.Qin.idIndex.keys():
        atv = 0
        for i in range(self.keywordNum):
            atv += self.act[i][expNodeId]
        self.activation[0][expNodeId] = atv
        if expNodeId in self.Qin.idIndex.keys():
            self.Qin.pushAndChange(HeapNode(expNodeId, atv))

        nodeName = self.kg.entities_id_dict.get(expNodeId)
        ancestors = self.kg.hr_dict.get(nodeName)
        if ancestors is None:
            return

        for node in ancestors:
            ancestorExpNodeNmae = node[0]
            ancestorExpNodeId = self.kg.reversed_entities_id_dict.get(ancestorExpNodeNmae)
            if self.act[i][ancestorExpNodeId] > 0:
                self.act[i][ancestorExpNodeId] = (1 - self.mu) * self.act[i][expNodeId] / nodeSetSiza

