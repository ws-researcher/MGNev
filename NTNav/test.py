# from KeywordSearch.NTNav.CreatMateGraphIndex import MeatPathNode
from RDFFile2Graph.ReadRDFFile import ReadRDFFile
from KeywordSearch.NTNav.NTNav import *
from RDFFile2Graph.Kg import KG

# r1 = ReadRDFFile()
# kg = KG()
# r1.file2graph(kg, "D:/workplace/python/KeywordSearch/dataSet/CTIKG/CyberSecurity.nt")
#
#
# Key = NTNav(kg, ["WannaCry","Attack Pattern", "platform"])
# # Key = NTNav(kg, ["WannaCry","Attack Pattern"])
# # Key = NTNav(kg, ["BlackEnergy","system","Vulnerability"])
# # Key = NTNav(kg, ["BlackEnergy","ApplicablePlatform","Weakness"])
# Key.search()









# r1 = ReadRDFFile()
# kg = KG()
# # r1.file2graph(kg, "D:/ws/aa/KeywordSearch/dataSet/CTIKG/CyberSecurity.nt")
# r1.file2graph(kg, "D:/ws/aa/KeywordSearch/dataSet/CTIKG/CTIKG.nt")
#
#
# # Key = NTNav(kg, ["WannaCry","Attack Pattern", "platform"])
# print("entities_set" + str(sys.getsizeof(kg.entities_set)))
# print("relations_set" + str(sys.getsizeof(kg.relations_set)))
# print("rev_hr_dict" + str(sys.getsizeof(kg.rev_hr_dict)))
# print("rev_rt_dict" + str(sys.getsizeof(kg.rev_rt_dict)))
# Key = NTNav(kg, ["WannaCry","Attack Pattern"])
# # Key = NTNav(kg, ["BlackEnergy","system","Vulnerability"])
# # Key = NTNav(kg, ["BlackEnergy","ApplicablePlatform","Weakness"])
# Key.search()



kg = KG()
r = ReadRDFFile()
r.file2graph(kg, "D:/ws/aa/KeywordSearch/dataSet/Yago4/yago-wd-class.nt")
r.file2graph(kg, "D:/ws/aa/KeywordSearch/dataSet/Yago4/yago-wd-full-types.nt")
r.file2graph(kg, "D:/ws/aa/KeywordSearch/dataSet/Yago4/yago-wd-facts.nt")
# print("entities_set" + str(sys.getsizeof(kg.entities_set)))
# print("relations_set" + str(sys.getsizeof(kg.relations_set)))
# print("rev_hr_dict" + str(sys.getsizeof(kg.rev_hr_dict)))
# print("rev_rt_dict" + str(sys.getsizeof(kg.rev_rt_dict)))
Key = NTNav(kg,["Amit Singhal","Google"])
Key.search()