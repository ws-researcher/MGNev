import numpy as np
import pandas as pd
from KeywordSearch.Util.keywordMatch import keywordMatch
from KeywordSearch.Util.AnswerTree import AnswerTree
from queue import PriorityQueue
from KeywordSearch.KeyKG.Util import *
from random import choice
from datetime import *

class KeyKG:

    def __init__(self, kg, keywordList=[]):
        self.kg = kg
        self.keywordList = keywordList

        self.nodeNum = self.kg.entities_num
        self.keywordNum = len(self.keywordList)

        km = keywordMatch(kg, self.keywordList)
        self.kgSearchNodeIdList, self.kgSearchNodeNameList = km.kwMatch()

        # self.kfullNmae = list(self.kg.entities_id_dict.get(x) for s in self.kgSearchNodeIdList for x in s)

        path = './HL.csv'
        self.staticHL = self.HLReload(path=path)

        self.M = self.construct(self.staticHL, self.keywordList)

    def search(self):
        dt1 = datetime.now()

        # K1 = self.kgSearchNodeIdList[0]
        K1 = self.kgSearchNodeIdList[0]

        T = pd.DataFrame(index=K1, columns=['w', 'u'])
        for v1 in K1:
            Uv1 = set()
            w = 0
            # Lv1 = self.staticHL[v1]
            for i in self.keywordList[1:]:
                vi = self.getvi(self.M, [i], v1)
                # Uv1.append(vi)
                Uv1 |= set(vi)
                w += choice(vi).dist

                # v = list(self.kgSearchNodeIdList[i])
                # disList = list(map(self.getD, v1, v))
                # index = np.argmin(disList)
                # vi = v[index]
                # Uv1.append(vi)
                # w += self.getD(v1, vi)
            T['u'][v1] = Uv1
            T['w'][v1] = w

        x = np.argmin(T['w'])

        Ux = T['u'][x]
        answerQueue = PriorityQueue()
        for u in Ux:
            VTu = set()
            VTu.add(u)
            Mu = self.constructMu(VTu)
            answer = AnswerTree()
            while not Ux.issubset(VTu):
                remainUx = Ux - VTu
                remainUx = list(remainUx)

                smin = None
                tmin = None
                dis = float('inf')
                for t in remainUx:
                    tid = t.pred
                    index = list(map(lambda x: x.pred, VTu))
                    si = self.getvi(Mu, index, tid)
                    if si[0].dist < dis:
                        smin = si
                        tmin = tid

                paths = self.getSP(smin, tmin)

                for path in paths:
                    VTu |= set(path)

                Mu = self.constructMu(VTu)

                for path in paths:
                    answer.addPath(self.kg, path)
                    answer.score = len(answer.edges)

            answerQueue.put(answer)


            #     remainUx = Ux - VTu
            #     remainUx = list(remainUx)
            #     VTul = list(VTu)
            #     data = [[self.getD(x, y) for x in VTul] for y in remainUx]
            #     Vmin = pd.DataFrame(data, index=VTul, columns=remainUx)
            #     minIndex = Vmin.stack().idxmin()
            #     path = self.getSP(minIndex[0], minIndex[1])
            #     VTu |= set(path)
            #     answer.addPath(self.kg, path)
            #     answer.score = len(answer.edges)
            #
            # answerQueue.put(answer)
        dt2 = datetime.now()
        dtc = dt2 - dt1
        print(dtc.microseconds)
        return answerQueue

    def getvi(self, M, mIndex, v1):
        Lv1 = self.staticHL[v1]
        distSet = set()
        Mi = M.loc[mIndex, list(Lv1.keys())]
        d = Mi.applymap(lambda x: HLHop(x[0], x[1]))
        for h in Lv1.keys():
            Lh = self.staticHL[h]
            dvh = min(Lh, key=Lh.get)
            dvhHop = Lh[dvh]
            dmh = d[h].min()
            dh = HLHop(dmh.dist + dvhHop.dist, h)
            distSet.add(dh)

        minvi = min(distSet)
        vi = [v for v in distSet if v.dist == minvi.dist]
        return vi

    def getSP(self, node1, node2):
        path = []
        L1 = self.staticHL[node1]
        L2 = self.staticHL[node2]
        h1 = set(L1.keys()) & set(L2.keys())
        print("s")
        for h in h1:
            Lh = self.staticHL[h]

        # for n in nodeList1:
        #     pathi = [n]
        #     nextNode = n
        #     while nextNode.pred != node:
        #         pathi.append(nextNode.pred)
        #         nextNode = nextNode.pred
        #     path.append(pathi)

        return path

    def construct(self, staticHL, keywordList):
        entitiesIds = list(self.kg.entities_id_dict.keys())
        # entitiesIds = self.kg.entities_list
        ix = keywordList[1:]
        M = pd.DataFrame(index=ix, columns=entitiesIds)

        for index in ix:
            i = keywordList.index(index)
            for node in entitiesIds:
                # minDistNode = findMinPathNode(staticHL, node, self.kgSearchNodeIdList[i])
                minDistNode = findMinPathNode(staticHL, node, self.kgSearchNodeIdList[i])
                M[node][index] = (minDistNode.dist, minDistNode.pred)

        return M

    def constructMu(self, VTu):
        idSet = set()
        for n in VTu:
            idSet.add(n.pred)

        entitiesIds = list(self.kg.entities_id_dict.keys())
        Mu = pd.DataFrame(index=list(idSet), columns=entitiesIds)
        for node in entitiesIds:
            for id in idSet:
                minDistNode = findMinPathNode(self.staticHL, node, [id])
                Mu[node][id] = (minDistNode.dist, minDistNode.pred)

        return Mu
    def HLReload(self, path: str):
        staticHL = pd.read_csv(path, index_col=0)
        staticHL = staticHL['this'].map(eval)
        staticHL = staticHL.map(self.toHLHop)
        # print(staticHL.index)
        staticHL.index = staticHL.index.map(self.kg.reversed_entities_id_dict.get)
        # print(staticHL.index)

        return staticHL

    def toHLHop(self, oneDict):
        for key in oneDict.keys():
            value = oneDict[key]
            oneDict[key] = HLHop(value[0], self.kg.reversed_entities_id_dict.get(value[1]))
            # oneDict[key] = HLHop(value[0], value[1])
        return oneDict
