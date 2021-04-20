from RDFFile2Graph.Kg import KG
import csv

from RDFFile2Graph.ReadRDFFile import ReadRDFFile


def CreatKeywordIndex(kg:KG):
    entitiesList = kg.entities_list
    relationsList = kg.relations_list
    attributesList = kg.attributes_list


    with open("keywordIndex.csv", "w", encoding='utf-8') as keywordIndexFile:
        writer = csv.writer(keywordIndexFile)


        for entity in entitiesList:
            keywordSet = kg.ha_dict.get((entity, 'http://www.w3.org/2000/01/rdf-schema#label'), set())
            label = str(entity).split('/')[-1]
            # e_id = kg.reversed_entities_id_dict.get(entity)
            keywordSet.add(label)
            writer.writerow([keywordSet, entity])

        for relation in relationsList:
            label = str(relation).split('/')[-1]
            # r_id = kg.reversed_relations_id_dict.get(relation)
            writer.writerow([label, relation])

        for attribute in attributesList:
            label = str(attribute).split('/')[-1]
            # a_id = kg.reversed_attributes_id_dict.get(attribute)
            writer.writerow([label, attribute])


kg = KG()
r = ReadRDFFile()
r.file2graph(kg, "D:/workplace/python/KeywordSearch/dataSet/CTIKG/CyberSecurity.nt")
CreatKeywordIndex(kg)