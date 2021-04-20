import rdflib
import os
from RDFFile2Graph.Kg import KG

class ReadRDFFile:
    # def __init__(self, filePath, format=None):
    #     self.fileType = format
    #     self.filePath = filePath
    #
    #     if os.path.exists(filePath):
    #         head, tail = os.path.split(filePath)
    #
    #         # NT
    #         if tail.endswith(".nt") and format is None:
    #             self.fileType = "ntriples"
    #         # RDF/XML
    #         if tail.endswith(".rdf") and format is None:
    #             self.fileType = "turtle"
    #         # N3
    #         if tail.endswith(".n3") and format is None:
    #             self.fileType = "n3"
    #         # N3
    #         if tail.endswith(".xml") and format is None:
    #             self.fileType = "xml"
    #     else:
    #         print(filePath + 'file is not exist')



    def file2graph(self, kg:KG, filePath, format='nt'):
        g = rdflib.Graph()
        g.parse(filePath, format=format)

        relation_triples, attribute_triples = set(), set()

        # 循环遍历图谱中每一个三元组
        for subj, pred, obj in g:
            # 空图谱检查
            if (subj, pred, obj) not in g:
                raise Exception("It better be!")

            if isinstance(obj, rdflib.term.URIRef):
                triple = (str(subj).split('/')[-1], str(pred).split('/')[-1], str(obj).split('/')[-1])
                # triple = (str(subj).split('/')[-1], str(pred).split('/')[-1], str(obj).split('/')[-1])
                relation_triples.add(triple)
            elif isinstance(obj, rdflib.term.Literal):
                triple = (str(subj).split('/')[-1], str(pred).split('/')[-1], str(obj).split('/')[-1])
                # triple = (str(subj).split('/')[-1], str(pred).split('/')[-1], str(obj).split('/')[-1])
                attribute_triples.add(triple)

        kg.add_relations(relation_triples)
        kg.add_attributes(attribute_triples)
        # return kg

# r = ReadRDFFile("../dataSet/CyberSecurity.nt")
# kg = r.file2graph()
