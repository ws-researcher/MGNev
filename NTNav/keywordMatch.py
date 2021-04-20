# 关键字匹配图谱中的实体
import Levenshtein
from RDFFile2Graph.Kg import KG
from KeywordSearch.NTNav.Util import *

class keywordMatch:
    def __init__(self, kg : KG, keywordList = [], ontologyClass = []):
        self.kg = kg
        self.keywordList = keywordList
        self.ontologyClass = ontologyClass
        # 关键字匹配相似度阈值
        self.matchNum = 0.7

        self.rootClass = 'http://www.w3.org/2000/01/rdf-schema#Class'

        self.Property = {'http://www.w3.org/2002/07/owl#ObjectProperty', 'http://www.w3.org/2002/07/owl#FunctionalProperty', 'http://www.w3.org/2002/07/owl#DatatypeProperty'}


    def matchNTClass(self):
        kgSearchNodeNameList = []
        kgSearchNodeIdList = []
        index = self.getindex()
        for keyword in self.keywordList:
            keyword = str(keyword).lower()
            l = list(map(lambda x: (self.wordSimilarity(keyword, x[0]), x[1]), index))
            l = list(x for x in l if x[0] is not None)
            SiId = set()
            SiName = set()
            for s in l:
                SiId.add(s[1])
                SiName.add(s[0])
                if len(SiId) >=3:
                    break

            kgSearchNodeNameList.append(SiName)
            kgSearchNodeIdList.append(SiId)

        return kgSearchNodeIdList, kgSearchNodeNameList


    def getindex(self):
        wordIndex = list()

        entitiesList = self.kg.entities_set
        relationsList = self.kg.relations_set
        attributesList = self.kg.attributes_set

        for entity in entitiesList:
            keywordSet = self.kg.ha_dict.get((entity, 'http://www.w3.org/2000/01/rdf-schema#label'), set())
            keywordClassSet = self.kg.rev_hr_dict.get((entity, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), set())
            keywordOntologyClassSet = set()
            ontologyClass = self.ontologyClass
            for Class in keywordClassSet:
                subclasses = {Class}
                while subclasses:
                    for subclass in subclasses:
                        if subclass not in ontologyClass:
                            subclasses.remove(subclass)
                            subclasses |= self.kg.rev_hr_dict.get((entity, 'http://www.w3.org/2000/01/rdf-schema#subClassOf'), set())
                        else:
                            subclasses.remove(subclass)
                            keywordOntologyClassSet.add(subclass)


            label = str(entity).split('/')[-1]
            e_id = self.kg.reversed_entities_id_dict.get(entity)
            keywordSet.add(label)

            for Class in keywordOntologyClassSet:
                if Class != self.rootClass:
                    ClassId = self.kg.reversed_entities_id_dict.get(Class)
                    ss = (keywordSet, IdClassType(e_id, ClassId, NodeType.entity))
                    wordIndex.append(ss)
                elif Class in self.Property:
                    pass
                else:
                    ss = (keywordSet, IdClassType(None, e_id, NodeType.entity))
                    wordIndex.append(ss)

        for relation in relationsList:
            label = str(relation).split('/')[-1]
            r_id = self.kg.reversed_relations_id_dict.get(relation)
            wordIndex.append(([label], IdClassType(None, r_id, NodeType.relation)))

        for attribute in attributesList:
            label = str(attribute).split('/')[-1]
            a_id = self.kg.reversed_attributes_id_dict.get(attribute)
            wordIndex.append(([label], IdClassType(None, a_id, NodeType.attribution)))

        return wordIndex

    def wordSimilarity(self, word = '', wordList = []):
        sl = list(map(lambda x: (x, Levenshtein.ratio(word, x)), wordList))
        s = sorted(sl, key=lambda x: x[1], reverse = True)[0]
        if s[1] > self.matchNum:
            return s[0]
        else:
            return None