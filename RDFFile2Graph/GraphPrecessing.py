import rdflib
import os
import re

from rdflib import URIRef, Graph, BNode

from RDFFile2Graph.Kg import KG
from KeywordSearch.Util.Util import Stack


class GraphPrecessing:

    def __init__(self, kg:KG):
        self.kg = kg


    def isBlankNode(self, o: URIRef):
        res = re.match('http://', str(o))
        if res is None:
            return True
        else:
            return False

    def isRdfNode(self, o: URIRef):
        res = re.match('http://www.w3.org/1999/02/22-rdf-syntax-ns#', str(o))
        if res is None:
            return False
        else:
            return True

    def isOwlNode(self, o: URIRef):
        res = re.match('http://www.w3.org/2002/07/owl#', str(o))
        if res is None:
            return False
        else:
            return True

    def findChildren(self, node, g:Graph):
        children = set()
        for s, p, o in g.triples((node, None, None)):
            children.add(o)
        return children

    def BFS(self, root: URIRef, g:Graph):
        res = set()
        visitedNode = set()
        visiteNode = Stack()
        visiteNode.push(root)
        while not visiteNode.is_empty():
            node = visiteNode.pop()

            if self.isBlankNode(node) and node not in visitedNode:
                for s, p, o in g.triples((node, None, None)):
                    isRdfOrOwl = self.isRdfNode(o) or self.isOwlNode(o)
                    if not isRdfOrOwl:
                        visiteNode.push(o)
            else:
                res.add(node)

            visitedNode.add(node)
        return res


    def ontologyPrecess(self, filePath, format='nt'):
        rmObSet = {'http://schema.org/Thing', 'http://www.w3.org/2002/07/owl#Class', 'http://www.w3.org/2002/07/owl#DatatypeProperty', 'http://www.w3.org/2002/07/owl#FunctionalProperty', 'http://www.w3.org/2002/07/owl#ObjectProperty'}
        rmrelSet = {'http://www.w3.org/2000/01/rdf-schema#range', 'http://www.w3.org/2000/01/rdf-schema#domain', 'http://www.w3.org/2000/01/rdf-schema#subPropertyOf'}
        g = rdflib.Graph()
        g.parse(filePath, format=format)

        relation_triples, attribute_triples = set(), set()

        classSet = set()
        propertySet = set()
        attributeSet = set()

        for subj, pred, obj in g:

            # 空图谱检查
            if (subj, pred, obj) not in g:
                raise Exception("It better be!")

            if isinstance(obj, rdflib.term.URIRef):
                if str(obj) == 'http://www.w3.org/2002/07/owl#Class' and not isinstance(subj, BNode):
                    classSet.add(subj)
                elif str(obj) == 'http://www.w3.org/2002/07/owl#ObjectProperty':
                    propertySet.add(subj)
                elif str(obj) == 'http://www.w3.org/2002/07/owl#DatatypeProperty':
                    attributeSet.add(subj)


        subClassOf = URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf")
        range = URIRef("http://www.w3.org/2000/01/rdf-schema#range")
        domain = URIRef("http://www.w3.org/2000/01/rdf-schema#domain")
        for pro in propertySet:
            if str(pro) == 'http://schema.org/award':
                print('s')
            heads = set()
            tails = set()
            for s, p, o in g.triples((pro, range, None)):
                isBlank = self.isBlankNode(o)
                if isBlank:
                    tails |= self.BFS(o, g)
                else:
                    tails.add(o)
            for s, p, o in g.triples((pro, domain, None)):
                isBlank = self.isBlankNode(o)
                if isBlank:
                    heads |= self.BFS(o, g)
                else:
                    heads.add(o)
            for head in heads:
                for tail in tails:
                    triple = (str(head).split('/')[-1], str(pro).split('/')[-1], str(tail).split('/')[-1])
                    relation_triples.add(triple)

        for attribute in attributeSet:
            for s, p, o in g.triples((attribute, domain, None)):
                if o in classSet:
                    triple = (str(o).split('/')[-1], str(s).split('/')[-1], None)
                    attribute_triples.add(triple)

        for s, p, o in g.triples((None, subClassOf, None)):
            triple = (str(s).split('/')[-1], str(p).split('/')[-1], str(o).split('/')[-1])
            relation_triples.add(triple)

        self.kg.add_relations(relation_triples)
        self.kg.add_attributes(attribute_triples)
        # return kg
