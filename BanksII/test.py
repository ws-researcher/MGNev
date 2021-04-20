from RDFFile2Graph.Kg import KG
from RDFFile2Graph.ReadRDFFile import ReadRDFFile
from KeywordSearch.BanksII.BanksTwo import BanksT


# r1 = ReadRDFFile()
# kg = KG()
# r1.file2graph(kg, "D:/ws/aa/KeywordSearch/dataSet/CTIKG/CyberSecurity.nt")
#
# banks = BanksT(kg,["WannaCry","Attack Pattern"])
# banks.search()



kg = KG()
r = ReadRDFFile()
r.file2graph(kg, "D:/ws/aa/KeywordSearch/dataSet/Yago4/yago-wd-class.nt")
r.file2graph(kg, "D:/ws/aa/KeywordSearch/dataSet/Yago4/yago-wd-full-types.nt")
r.file2graph(kg, "D:/ws/aa/KeywordSearch/dataSet/Yago4/yago-wd-facts.nt")
# print("entities_set" + str(sys.getsizeof(kg.entities_set)))
# print("relations_set" + str(sys.getsizeof(kg.relations_set)))
# print("rev_hr_dict" + str(sys.getsizeof(kg.rev_hr_dict)))
# print("rev_rt_dict" + str(sys.getsizeof(kg.rev_rt_dict)))
banks = BanksT(kg,["Amit Singhal","Google"])
banks.search()