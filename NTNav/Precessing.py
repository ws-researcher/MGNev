from RDFFile2Graph.Kg import KG
from RDFFile2Graph.ReadRDFFile import ReadRDFFile

kg = KG()
r = ReadRDFFile()
r.file2graph(kg, "D:/workplace/python/KeywordSearch/dataSet/Yago4/yago-wd-schema.nt")
r.file2graph(kg, "D:/workplace/python/KeywordSearch/dataSet/Yago4/yago-wd-class.nt")
r.file2graph(kg, "D:/workplace/python/KeywordSearch/dataSet/Yago4/yago-wd-full-types.nt")
# r.file2graph(kg, "D:/workplace/python/KeywordSearch/dataSet/Yago4/yago-wd-facts.nt")