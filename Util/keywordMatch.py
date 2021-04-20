# 关键字匹配图谱中的实体
import Levenshtein
from RDFFile2Graph.Kg import KG

class keywordMatch:
    def __init__(self, kg : KG, keywordList = []):
        self.kg = kg
        self.keywordList = keywordList
        # 关键字匹配相似度阈值
        self.matchNum = 0.7


    def kwMatch(self):
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
        # relationsList = self.kg.relations_list
        attributesList = self.kg.attributes_set

        for entity in entitiesList:
            # keywordSet = self.kg.ha_dict.get((entity, 'http://WS_Research.org/CyberSecurity/name'), set())
            # keywordSet |= self.kg.ha_dict.get((entity, 'http://www.w3.org/2000/01/rdf-schema#label'), set())
            keywordSet = self.kg.ha_dict.get((entity, 'name'), set())
            keywordSet |= self.kg.ha_dict.get((entity, 'rdf-schema#label'), set())
            # label = str(entity)
            label = str(entity).split('/')[-1]
            e_id = self.kg.reversed_entities_id_dict.get(entity)
            keywordSet.add(label)
            ss = (keywordSet, e_id)
            wordIndex.append(ss)

        # for relation in relationsList:
        #     label = str(relation).split('/')[-1]
        #     r_id = self.kg.reversed_relations_id_dict.get(relation)
        #     wordIndex.append(([label], r_id))

        for attribute in attributesList:
            # label = str(attribute)
            label = str(attribute).split('/')[-1]
            a_id = self.kg.reversed_attributes_id_dict.get(attribute)
            wordIndex.append(([label], a_id))

        return wordIndex

    def wordSimilarity(self, word = '', wordList = []):
        sl = list(map(lambda x: (x, Levenshtein.ratio(word, x)), wordList))
        s = sorted(sl, key=lambda x: x[1], reverse = True)[0]
        if s[1] > self.matchNum:
            return s[0]
        else:
            return None