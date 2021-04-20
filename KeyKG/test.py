from RDFFile2Graph.Kg import KG
from RDFFile2Graph.ReadRDFFile import ReadRDFFile
from KeywordSearch.KeyKG.KeyKG import KeyKG
# from KeywordSearch.KeyKG.ConstructStaticHL import ConstructStaticHL



r1 = ReadRDFFile()
kg = KG()
r1.file2graph(kg, "D:/ws/aa/KeywordSearch/dataSet/CTIKG/CyberSecurity.nt")
Key = KeyKG(kg,["WannaCry","Attack Pattern"])
Key.search()

# H = ConstructStaticHL(kg)
# H.constructStaticHL()'