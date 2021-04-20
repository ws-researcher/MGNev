#coding=utf-8

from rdflib import URIRef, BNode, Literal,Graph
from rdflib.namespace import RDF,OWL,RDFS,XSD
from rdflib import Namespace


import json
import glob

import csv

CS = Namespace("http://WS_Research.org/CyberSecurity/")
CyberSecurityKG = Graph()
# ---------------class name--------------------------------------
AttackPattern = URIRef("http://WS_Research.org/CyberSecurity/AttackPattern")

IntrusionSet = URIRef("http://WS_Research.org/CyberSecurity/IntrusionSet")

Malware = URIRef("http://WS_Research.org/CyberSecurity/Malware")

Tool = URIRef("http://WS_Research.org/CyberSecurity/Tool")

Weakness = URIRef("http://WS_Research.org/CyberSecurity/Weakness")

Vulnerability = URIRef("http://WS_Research.org/CyberSecurity/Vulnerability")

Indicator = URIRef("http://WS_Research.org/CyberSecurity/Indicator")

CourseOfAction = URIRef("http://WS_Research.org/CyberSecurity/CourseOfAction")

ApplicablePlatform = URIRef("http://WS_Research.org/CyberSecurity/ApplicablePlatform")


Observable = URIRef("http://WS_Research.org/CyberSecurity/Observable")

CyberAction = URIRef("http://WS_Research.org/CyberSecurity/CyberAction")

Campaign = URIRef("http://WS_Research.org/CyberSecurity/Campaign")

# ---------------class name--------------------------------------

# --------------object properties name-----------------------------------
uses = URIRef("http://WS_Research.org/CyberSecurity/uses")

targets = URIRef("http://WS_Research.org/CyberSecurity/targets")

platform = URIRef("http://WS_Research.org/CyberSecurity/platform")

mitigates = URIRef("http://WS_Research.org/CyberSecurity/mitigates")

attributed_to = URIRef("http://WS_Research.org/CyberSecurity/attributed_to")

led_Consequences = URIRef("http://WS_Research.org/CyberSecurity/led_Consequences")

indicates = URIRef("http://WS_Research.org/CyberSecurity/indicates")

derived_from = URIRef("http://WS_Research.org/CyberSecurity/derived_from")

affected_resources = URIRef("http://WS_Research.org/CyberSecurity/affected_resources")

can_also_be = URIRef("http://WS_Research.org/CyberSecurity/can_also_be")

can_follow = URIRef("http://WS_Research.org/CyberSecurity/can_follow")

can_precede = URIRef("http://WS_Research.org/CyberSecurity/can_precede")

child_of = URIRef("http://WS_Research.org/CyberSecurity/child_of")

parent_of = URIRef("http://WS_Research.org/CyberSecurity/parent_of")

peer_of = URIRef("http://WS_Research.org/CyberSecurity/peer_of")

starts_with = URIRef("http://WS_Research.org/CyberSecurity/starts_with")

partOf = URIRef("http://WS_Research.org/CyberSecurity/partOf")

required_by = URIRef("http://WS_Research.org/CyberSecurity/required_by")

requires = URIRef("http://WS_Research.org/CyberSecurity/requires")

required_resources = URIRef("http://WS_Research.org/CyberSecurity/required_resources")

is_Instance_Of = URIRef("http://WS_Research.org/CyberSecurity/is_Instance_Of")

downloads = URIRef("http://WS_Research.org/CyberSecurity/downloads")


delivers = URIRef("http://WS_Research.org/CyberSecurity/delivers")


installs = URIRef("http://WS_Research.org/CyberSecurity/installs")


execute = URIRef("http://WS_Research.org/CyberSecurity/execute")


intervalBefore = URIRef("http://WS_Research.org/CyberSecurity/intervalBefore")


# --------------object properties name-----------------------------------


# --------------data properties name-------------------------------------
name = URIRef("http://WS_Research.org/CyberSecurity/name")



aliases = URIRef("http://WS_Research.org/CyberSecurity/aliases")


description = URIRef("http://WS_Research.org/CyberSecurity/description")


introduction_phase = URIRef("http://WS_Research.org/CyberSecurity/introduction_phase")

likelihood_Of_Exploit = URIRef("http://WS_Research.org/CyberSecurity/likelihood_Of_Exploit")


ordinality = URIRef("http://WS_Research.org/CyberSecurity/ordinality")


functional_Area = URIRef("http://WS_Research.org/CyberSecurity/functional_Area")


# backgroundDetails = URIRef("http://WS_Research.org/CyberSecurity/background_details")
# CyberSecurityKG.add((backgroundDetails,RDF.term("type"),RDF.term("predicate")))
# CyberSecurityKG.add((backgroundDetails,RDFS.term("domain"),Weakness))
# CyberSecurityKG.add((backgroundDetails,RDFS.term("range"),XSD.term("string")))

effectiveness = URIRef("http://WS_Research.org/CyberSecurity/effectiveness")


mitigation_Phase = URIRef("http://WS_Research.org/CyberSecurity/mitigation_Phase")


mitigation_Strategy = URIRef("http://WS_Research.org/CyberSecurity/mitigation_Strategy")


scope = URIRef("http://WS_Research.org/CyberSecurity/scope")


impact = URIRef("http://WS_Research.org/CyberSecurity/impact")


likelihood = URIRef("http://WS_Research.org/CyberSecurity/likelihood")


typical_Severity = URIRef("http://WS_Research.org/CyberSecurity/typical_Severity")


likelihood_Of_Attack = URIRef("http://WS_Research.org/CyberSecurity/likelihood_Of_Attack")




prerequisites = URIRef("http://WS_Research.org/CyberSecurity/prerequisites")


skills_Required = URIRef("http://WS_Research.org/CyberSecurity/skills_Required")


# exampleInstances = URIRef("http://WS_Research.org/CyberSecurity/exampleInstances")
# CyberSecurityKG.add((exampleInstances,RDF.term("type"),RDF.term("predicate")))
# CyberSecurityKG.add((exampleInstances,RDFS.term("domain"),AttackPattern))
# CyberSecurityKG.add((exampleInstances,RDFS.term("range"),XSD.term("string")))

execution_Flow = URIRef("http://WS_Research.org/CyberSecurity/execution_Flow")


step = URIRef("http://WS_Research.org/CyberSecurity/step")


attack_Phase = URIRef("http://WS_Research.org/CyberSecurity/attack_Phase")


attack_description = URIRef("http://WS_Research.org/CyberSecurity/attack_description")


resources_Required = URIRef("http://WS_Research.org/CyberSecurity/resources_Required")



permissions_Required = URIRef("http://WS_Research.org/CyberSecurity/permissions_Required")


# phases = URIRef("http://WS_Research.org/CyberSecurity/phases")
# CyberSecurityKG.add((phases,RDF.term("type"),RDF.term("predicate")))
# CyberSecurityKG.add((phases,RDFS.term("domain"),AttackPattern))
# CyberSecurityKG.add((phases,RDFS.term("range"),XSD.term("string")))

detected_in = URIRef("http://WS_Research.org/CyberSecurity/detected_in")


bypass = URIRef("http://WS_Research.org/CyberSecurity/bypass")


achieve = URIRef("http://WS_Research.org/CyberSecurity/achieve")

# --------------data properties name-------------------------------------



# --------------construct ontology graph--------------------------

CyberSecurityKG.add((Malware,uses,AttackPattern))
# CyberSecurityKG.add((Tool,uses,AttackPattern))

CyberSecurityKG.add((IntrusionSet,uses,AttackPattern))
CyberSecurityKG.add((IntrusionSet,uses,Malware))
CyberSecurityKG.add((IntrusionSet,uses,Tool))
CyberSecurityKG.add((CyberAction,uses,Tool))

CyberSecurityKG.add((AttackPattern,targets,Weakness))
CyberSecurityKG.add((CyberAction,targets,Vulnerability))
CyberSecurityKG.add((Campaign,targets,ApplicablePlatform))

# CyberSecurityKG.add((Weakness,related_Weakness,Weakness))
# CyberSecurityKG.add((Weakness,child_of,Weakness))
# CyberSecurityKG.add((Weakness,parent_of,Weakness))
# CyberSecurityKG.add((Weakness,starts_with,Weakness))
# CyberSecurityKG.add((Weakness,can_follow,Weakness))
# CyberSecurityKG.add((Weakness,can_precede,Weakness))
# CyberSecurityKG.add((Weakness,required_by,Weakness))
# CyberSecurityKG.add((Weakness,requires,Weakness))
# CyberSecurityKG.add((Weakness,can_also_be,Weakness))
# CyberSecurityKG.add((Weakness,peer_of,Weakness))

# CyberSecurityKG.add((AttackPattern,related_AttackPattern,AttackPattern))
# CyberSecurityKG.add((AttackPattern,child_of,AttackPattern))
# CyberSecurityKG.add((AttackPattern,parent_of,AttackPattern))
# CyberSecurityKG.add((AttackPattern,can_follow,AttackPattern))
# CyberSecurityKG.add((AttackPattern,can_precede,AttackPattern))
# CyberSecurityKG.add((AttackPattern,can_also_be,AttackPattern))
# CyberSecurityKG.add((AttackPattern,peer_of,AttackPattern))


CyberSecurityKG.add((Malware,platform,ApplicablePlatform))
CyberSecurityKG.add((Tool,platform,ApplicablePlatform))
CyberSecurityKG.add((AttackPattern,platform,ApplicablePlatform))

CyberSecurityKG.add((CourseOfAction,mitigates,AttackPattern))
CyberSecurityKG.add((CourseOfAction,mitigates,Weakness))

# CyberSecurityKG.add((Weakness,located_at,ApplicablePlatforms))

CyberSecurityKG.add((AttackPattern,required_resources,Observable))

CyberSecurityKG.add((Indicator,indicates,AttackPattern))
# CyberSecurityKG.add((Indicator,indicates,Weakness))

CyberSecurityKG.add((Vulnerability,derived_from,Weakness))

CyberSecurityKG.add((Vulnerability,attributed_to,ApplicablePlatform))
CyberSecurityKG.add((Weakness,attributed_to,ApplicablePlatform))
CyberSecurityKG.add((IntrusionSet,attributed_to,Campaign))

CyberSecurityKG.add((Malware,downloads,Malware))
CyberSecurityKG.add((Malware,downloads,Tool))

# CyberSecurityKG.add((CyberAction,installs,Malware))
# CyberSecurityKG.add((CyberAction,installs,Malware))

CyberSecurityKG.add((CyberAction,delivers,Malware))
CyberSecurityKG.add((Malware,execute,CyberAction))
CyberSecurityKG.add((IntrusionSet,execute,CyberAction))
CyberSecurityKG.add((CyberAction,is_Instance_Of,AttackPattern))
CyberSecurityKG.add((CyberAction,intervalBefore,CyberAction))

CyberSecurityKG.add((AttackPattern,name,Literal("")))
CyberSecurityKG.add((IntrusionSet,name,Literal("")))
CyberSecurityKG.add((Malware,name,Literal("")))
CyberSecurityKG.add((Tool,name,Literal("")))
CyberSecurityKG.add((Weakness,name,Literal("")))
CyberSecurityKG.add((Vulnerability,name,Literal("")))
CyberSecurityKG.add((Indicator,name,Literal("")))
CyberSecurityKG.add((CourseOfAction,name,Literal("")))

CyberSecurityKG.add((IntrusionSet,aliases,Literal("")))
CyberSecurityKG.add((Malware,aliases,Literal("")))
CyberSecurityKG.add((Tool,aliases,Literal("")))
CyberSecurityKG.add((Weakness,aliases,Literal("")))

CyberSecurityKG.add((AttackPattern,description,Literal("")))
CyberSecurityKG.add((IntrusionSet,description,Literal("")))
CyberSecurityKG.add((Malware,description,Literal("")))
CyberSecurityKG.add((Tool,description,Literal("")))
CyberSecurityKG.add((Weakness,description,Literal("")))
CyberSecurityKG.add((Vulnerability,description,Literal("")))
CyberSecurityKG.add((Indicator,description,Literal("")))
CyberSecurityKG.add((CourseOfAction,description,Literal("")))
CyberSecurityKG.add((Campaign,description,Literal("")))

CyberSecurityKG.add((Weakness,introduction_phase,Literal("")))

CyberSecurityKG.add((Weakness,likelihood_Of_Exploit,Literal("")))

CyberSecurityKG.add((Weakness,ordinality,Literal("")))

CyberSecurityKG.add((Weakness,functional_Area,Literal("")))

CyberSecurityKG.add((Indicator,effectiveness,Literal("")))
CyberSecurityKG.add((CourseOfAction,effectiveness,Literal("")))

CyberSecurityKG.add((CourseOfAction,mitigation_Phase,Literal("")))

CyberSecurityKG.add((CourseOfAction,mitigation_Strategy,Literal("")))

CyberSecurityKG.add((AttackPattern,led_Consequences,Literal("")))
CyberSecurityKG.add((Weakness,led_Consequences,Literal("")))
CyberSecurityKG.add((Vulnerability,led_Consequences,Literal("")))

CyberSecurityKG.add((AttackPattern,typical_Severity,Literal("")))

CyberSecurityKG.add((AttackPattern,likelihood_Of_Attack,Literal("")))

CyberSecurityKG.add((AttackPattern,prerequisites,Literal("")))

CyberSecurityKG.add((AttackPattern,skills_Required,Literal("")))

CyberSecurityKG.add((AttackPattern,execution_Flow,Literal("")))

CyberSecurityKG.add((AttackPattern,resources_Required,Literal("")))

CyberSecurityKG.add((AttackPattern,permissions_Required,Literal("")))

# CyberSecurityKG.add((AttackPattern,phases,Literal("")))

CyberSecurityKG.add((AttackPattern,detected_in,Literal("")))
CyberSecurityKG.add((AttackPattern,bypass,Literal("")))
CyberSecurityKG.add((AttackPattern,achieve,Literal("")))

# --------------construct ontology graph--------------------------


# print (CyberSecurityKG.serialize(format='turtle'))
# CyberSecurityKG.serialize('CyberSecurity.rdf',format='turtle')
CyberSecurityKG.serialize('CTIO.nt',format='ntriples')


# g= Graph()
# g.parse('./CyberSecurity.nt', format = 'ntriples')
# print('s')

