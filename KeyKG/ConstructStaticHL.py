import math

from RDFFile2Graph.Kg import KG
import csv
import pandas as pd
import numpy as np
from queue import PriorityQueue
from KeywordSearch.KeyKG.MinHeap import *
from KeywordSearch.KeyKG.Util import *
from RDFFile2Graph.ReadRDFFile import ReadRDFFile


class ConstructStaticHL:

    def __init__(self, kg:KG):
        self.kg = kg
        self.Property = {'http://www.w3.org/2002/07/owl#ObjectProperty',
                         'http://www.w3.org/2002/07/owl#FunctionalProperty',
                         'http://www.w3.org/2002/07/owl#DatatypeProperty'}

    def constructStaticHL(self):

        entitiesIds = list(self.kg.entities_id_dict.keys())

        #排序  本代码无
        entitiesIds = self.sort(entitiesIds)

        for id in entitiesIds:
            name = self.kg.entities_id_dict.get(id)
            if name == 'http://WS_Research.org/CyberSecurity/likelihood_Of_Attack':
                print('s')
            keywordClassSet = self.kg.rev_hr_dict.get((name, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                                                      set())
            if keywordClassSet & self.Property:
                entitiesIds.remove(id)

        L = pd.DataFrame(index=entitiesIds, columns= ['last', 'this'])
        for id in entitiesIds:

            HLSet = L['last'][id]
            if math.isnan(HLSet):
                HLSet = HLHopSet()
                HLSet[id] = HLHop(0, id)
                L['last'][id] = HLSet.values

        for id in entitiesIds:
            print(id)
            L['this'] = L['last']
            vdata = np.zeros(len(entitiesIds))
            visited = pd.DataFrame(vdata, index=entitiesIds, columns=['bool'])

            d = pd.DataFrame(index=entitiesIds, columns=['dist'])
            for ii in entitiesIds:
                d['dist'][ii] = (float("inf"), id)
            d['dist'][id] = (0, id)

            PQ = MinHeap()
            PQ.pushAndChange(HeapNode(id, d['dist'][id]))

            while not PQ.isEmpty():
                u = PQ.pop()
                u = u.id
                visited['bool'][u] = 1

                vHopDict = L['last'][id]
                uHopDict = L['last'][u]
                intersection = set(vHopDict.keys()) & set(uHopDict.keys())
                if len(intersection) == 0:
                    minDistNode = HLHop(float('inf'), id)
                else:
                    distSet = set()
                    for iNode in intersection:
                        vOneHop = vHopDict[iNode]
                        uOneHop = uHopDict[iNode]
                        hop = HLHop(vOneHop.dist + uOneHop.dist, iNode)
                        distSet.add(hop)

                    minDistNode = min(distSet)

                distu = d['dist'][u]
                if distu[0] <= minDistNode.dist:
                    uHopDict = L['last'][u]
                    uHopDict[id] = HLHop(distu[0], distu[1])
                    L['this'][u] = uHopDict

                    NBR = self.kg.NBR(u)
                    for nNode in NBR:
                        newDist = 0
                        if visited['bool'][nNode] == 0:
                            uname = self.kg.entities_id_dict.get(u)
                            nNodeName = self.kg.entities_id_dict.get(nNode)

                            relation1 = self.kg.eer_dict.get((uname, nNodeName))
                            relation2 = self.kg.eer_dict.get((nNodeName, uname))
                            if relation1 is  None:
                                relation1 = set()
                            if relation2 is None:
                                relation2 = set()
                            relationW = relation1 | relation2

                            weight = 0
                            for rel in relationW:
                                weight += rel[1]
                            weight = weight/len(relationW)
                            duNew = d['dist'][u]
                            newDist = duNew[0] + weight

                            du = d['dist'][nNode]
                            if newDist < du[0]:
                                d['dist'][nNode] = (newDist, u)
                            if nNode not in PQ.idIndex:
                                PQ.pushAndChange(HeapNode(nNode, d['dist'][nNode]))

                visited['bool'][u] = 1
            # print(L['this'])
        L = L.applymap(self.deal)
        L.index = L.index.map(lambda x: self.kg.entities_id_dict.get(x))

        L['this'].to_csv("HL.csv", sep=',', header=True, index=True)
        return L['this']


    def deal(self, x):
        for i in x.keys():
            value = x[i]
            if isinstance(value, tuple):
                pass
            else:
                nodename = self.kg.entities_id_dict.get(value.pred)
                x[i] = (value.dist, nodename)
        return x


    def sort(self, list):
        return list
        pass



class HLHopSet:

    def __init__(self, values = None):
        if values is None:
            self.values = dict()
        else:
            self.values = values

    def __len__(self):
        return len(self.values)


    def __getitem__(self, key):
        return self.values.get(key)

# value : HLHop
    def __setitem__(self, key, value):
        self.values[key] = value



r1 = ReadRDFFile()
kg = KG()
# r1.file2graph(kg, "D:/workplace/python/KeywordSearch/dataSet/CTIKG/CyberSecurity.nt")
r1.file2graph(kg, "D:/workplace/python/KeywordSearch/dataSet/linkedmdb/linkedmdb-latest-dump.nt")

H = ConstructStaticHL(kg)
H.constructStaticHL()