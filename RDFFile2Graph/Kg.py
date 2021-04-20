import itertools as it
import hashlib
import sys


def parse_triples(triples):
    subjects, predicates, objects = set(), set(), set()
    for s, p, o in triples:
        subjects.add(s)
        predicates.add(p)
        objects.add(o)
    return subjects, predicates, objects


class KG:
    def __init__(self, relation_triples=set(), attribute_triples=set()):
        self.md5 = hashlib.md5()

        # 实体集
        self.entities_set, self.entities_list = set(), []
        self.entities_set = set()
        # 关系集
        self.relations_set, self.relations_list = set(), []
        self.relations_set = set()
        # 属性集
        self.attributes_set = set()
        self.attributes_set, self.attributes_list = set(), []
        # 实体、关系、属性数量
        self.entities_num, self.relations_num, self.attributes_num = None, None, None
        # 关系三元组数量、属性三元组数量
        self.relation_triples_num, self.attribute_triples_num = None, None
        # 本对象——关系三元组数量、属性三元组数量
        self.local_relation_triples_num, self.local_attribute_triples_num = None, None
        # ID : 实体
        self.entities_id_dict = dict()
        # ID ：关系
        self.relations_id_dict = dict()
        # ID ：属性
        self.attributes_id_dict = dict()
        # 实体:ID
        self.reversed_entities_id_dict = dict()
        # 关系:ID
        self.reversed_relations_id_dict = dict()
        # 属性:ID
        self.reversed_attributes_id_dict = dict()

        # rt_dict（头实体:（关系，尾实体, 边权重））、hr_dict（尾实体：（头实体，关系， 边权重））
        self.rt_dict, self.hr_dict = dict(), dict()
        # (头实体，尾实体) ： （关系， 边权重）
        self.eer_dict = dict()

        # 实体关系对
        self.entity_relations_dict = dict()
        # 实体属性对
        self.entity_attributes_dict = dict()
        #  头实体：（属性，值）
        self.av_dict = dict()
        # (头实体，关系)：尾实体集合
        self.rev_hr_dict = dict()
        # (关系, 尾实体)：头实体集合
        self.rev_rt_dict = dict()
        # (头实体，属性)：值集合
        self.ha_dict = dict()

        # 上层（network schema, ontology）实体关系、实体属性，
        # self.sup_relation_triples_set, self.sup_relation_triples_list = set(), []
        # self.sup_attribute_triples_set, self.sup_attribute_triples_list = set(), []

        # 关系三元组集
        self.relation_triples_set = set()
        # 属性三元组集
        self.attribute_triples_set = set()
        # 关系三元组列表
        self.relation_triples_list = []
        # 属性三元组列表
        self.attribute_triples_list = []

        # head: 三元组集
        self.ht_set = dict()
        # tail: 三元组集
        self.tt_set = dict()
        # relation: 三元组集
        self.rt_set = dict()
        # (h, t): 三元组
        self.htt_set = dict()
        # (t, h): 三元组
        self.tht_set = dict()
        # head: 属性三元组
        self.hat_set = dict()

        # 本对象 关系三元组、属性三元组 集合 列表（本对象：传入的集合或列表复制为本对象的属性，防止指向同一地址）
        self.local_relation_triples_set = set()
        self.local_relation_triples_list = []
        self.local_attribute_triples_set = set()
        self.local_attribute_triples_list = []

        self.add_relations(relation_triples)
        self.add_attributes(attribute_triples)

        # self.set_id_dict()

        # print()
        # print("KG statistics:")
        # print("Number of entities:", self.entities_num)
        # print("Number of relations:", self.relations_num)
        # print("Number of attributes:", self.attributes_num)
        # print("Number of relation triples:", self.relation_triples_num)
        # print("Number of attribute triples:", self.attribute_triples_num)
        # print("Number of local relation triples:", self.local_relation_triples_num)
        # print("Number of local attribute triples:", self.local_attribute_triples_num)
        # print()

    def add_relations(self, relation_triples):
        if relation_triples:
            new_relation_triples_set = set(relation_triples)
            add_relation_triples_set = new_relation_triples_set - self.relation_triples_set
            self.relation_triples_set |= add_relation_triples_set
            self.relation_triples_list.extend(list(add_relation_triples_set))
            self.local_relation_triples_set |= self.relation_triples_set
            self.local_relation_triples_list = self.relation_triples_list

            heads, relations, tails = parse_triples(self.relation_triples_set)
            entities_set = heads | tails
            add_entities_set = entities_set - self.entities_set
            add_relations_set = relations - self.relations_set
            self.entities_set |= add_entities_set
            self.relations_set |= add_relations_set
            self.entities_list.extend(list(add_entities_set))
            self.relations_list.extend(list(add_relations_set))

            # self.entities_set |= heads | tails
            # self.relations_set |= relations
            # self.entities_list = list(self.entities_set)
            # self.relations_list = list(self.relations_set)
            self.entities_num = len(self.entities_set)
            self.relations_num = len(self.relations_set)
            self.relation_triples_num = len(self.relation_triples_set)
            self.local_relation_triples_num = len(self.local_relation_triples_set)
            self.generate_relation_triple_dict()
            self.parse_relations()
        self.set_id_dict()
        # print("Number of entities:", self.entities_num)

    def add_attributes(self, attribute_triples):
        add_attribute_triples_set = set(attribute_triples) - self.attribute_triples_set
        self.attribute_triples_set |= add_attribute_triples_set
        self.attribute_triples_list.extend(list(add_attribute_triples_set))
        self.local_attribute_triples_set = self.attribute_triples_set
        self.local_attribute_triples_list = self.attribute_triples_list


        entities, attributes, values = parse_triples(self.attribute_triples_set)
        add_entities_set = set(entities) - self.entities_set
        add_attributes_set = set(attributes) - self.attributes_set
        self.entities_set |= add_entities_set
        self.attributes_set |= add_attributes_set
        self.entities_list.extend(list(add_entities_set))
        self.attributes_list.extend(list(add_attributes_set))
        self.entities_num = len(self.entities_set)
        self.attributes_num = len(self.attributes_set)

        # self.attributes_set |= attributes
        # self.attributes_list = list(self.attributes_set)
        # self.attributes_num = len(self.attributes_set)

        self.attribute_triples_num = len(self.attribute_triples_set)
        self.local_attribute_triples_num = len(self.local_attribute_triples_set)
        self.generate_attribute_triple_dict()
        self.parse_attributes()
        self.set_id_dict()

    def generate_relation_triple_dict(self):
        self.rt_dict, self.hr_dict, self.rev_hr_dict, self.rev_rt_dict = dict(), dict(), dict(), dict()
        for h, r, t in self.local_relation_triples_set:
            rt_set = self.rt_dict.get(h, set())
            rt_set.add((r, t, 1))
            self.rt_dict[h] = rt_set

            hr_set = self.hr_dict.get(t, set())
            hr_set.add((h, r, 1))
            self.hr_dict[t] = hr_set

            eer_set = self.eer_dict.get((h, t), set())
            eer_set.add((r, 1))
            self.eer_dict[(h, t)] = eer_set

            rev_hr_set = self.rev_hr_dict.get((h, r), set())
            rev_hr_set.add(t)
            self.rev_hr_dict[(h, r)] = rev_hr_set

            rev_rt_set = self.rev_rt_dict.get((r, t), set())
            rev_rt_set.add(h)
            self.rev_rt_dict[(r, t)] = rev_rt_set

            ht_set = self.ht_set.get(h, set())
            ht_set.add((h, r, t))
            self.ht_set[h] = ht_set

            tt_set = self.tt_set.get(t, set())
            tt_set.add((h, r, t))
            self.tt_set[t] = tt_set

            rt_set = self.rt_set.get(r, set())
            rt_set.add((h, r, t))
            self.rt_set[r] = rt_set

            tht_set = self.tht_set.get((t, h), set())
            tht_set.add((h, r, t))
            self.tht_set[(t, h)] = tht_set

            htt_set = self.htt_set.get((h, t), set())
            htt_set.add((h, r, t))
            self.htt_set[(t, h)] = htt_set

        # print("Number of rt_dict:", len(self.rt_dict))
        # print("Number of hr_dict:", len(self.hr_dict))
        # print("Number of hr_dict:", len(self.rev_hr_dict))

    def generate_attribute_triple_dict(self):
        self.av_dict, self.ha_dict = dict(), dict()
        for h, a, v in self.local_attribute_triples_set:
            av_set = self.av_dict.get(h, set())
            av_set.add((a, v))
            self.av_dict[h] = av_set
            rev_ha_set = self.ha_dict.get((h, a), set())
            rev_ha_set.add(v)
            self.ha_dict[(h, a)] = rev_ha_set

            hat_set = self.hat_set.get(h, set())
            hat_set.add((h, a, v))
            self.hat_set[h] = hat_set

        # print("Number of av_dict:", len(self.av_dict))
        # print("Number of ha_dict:", len(self.ha_dict))

    def parse_relations(self):
        self.entity_relations_dict = dict()
        for ent, rel, _ in self.local_relation_triples_set:
            rels = self.entity_relations_dict.get(ent, set())
            rels.add(rel)
            self.entity_relations_dict[ent] = rels
        # print("entity relations dict:", len(self.entity_relations_dict))

    def parse_attributes(self):
        self.entity_attributes_dict = dict()
        for ent, attr, _ in self.local_attribute_triples_set:
            attrs = self.entity_attributes_dict.get(ent, set())
            attrs.add(attr)
            self.entity_attributes_dict[ent] = attrs
        # print("entity attributes dict:", len(self.entity_attributes_dict))

    def set_id_dict(self):
        self.entities_id_dict = dict()
        self.reversed_entities_id_dict = dict()
        self.relations_id_dict = dict()
        self.reversed_relations_id_dict = dict()
        self.attributes_id_dict = dict()
        self.reversed_attributes_id_dict = dict()
        eid = 0
        for e in self.entities_set:
            if e is not None:
                md5 = hashlib.md5()
                md5.update(e.encode('utf-8'))
                e_id = "e" + md5.hexdigest()
                # e_id = "e" + str(eid)
                self.entities_id_dict[e_id] = e
                self.reversed_entities_id_dict[e] = e_id
                eid += 1

        rid = 0
        for r in self.relations_set:
            if r is not None:
                md5 = hashlib.md5()
                md5.update(r.encode('utf-8'))
                r_id = "r" + md5.hexdigest()
                # r_id = "r" + str(rid)
                self.relations_id_dict[r_id] = r
                self.reversed_relations_id_dict[r] = r_id
                rid += 1

        aid = 0
        for a in self.attributes_set:
            if a is not None:
                md5 = hashlib.md5()
                md5.update(a.encode('utf-8'))
                a_id = "a" + md5.hexdigest()
                # a_id = "a" + str(aid)
                self.attributes_id_dict[a_id] = a
                self.reversed_attributes_id_dict[a] = a_id
                aid += 1

    def add_sup_relation_triples(self, sup_relation_triples):

        self.add_relations(sup_relation_triples)
        self.sup_relation_triples_set = set(sup_relation_triples)
        self.sup_relation_triples_list = list(self.sup_relation_triples_set)
        self.set_id_dict()

    def add_sup_attribute_triples(self, sup_attribute_triples):
        self.add_attributes(sup_attribute_triples)
        self.sup_attribute_triples_set = set(sup_attribute_triples)
        self.sup_attribute_triples_list = list(self.sup_attribute_triples_set)
        self.set_id_dict()

    # neighbors’ id or name of node
    def NBR(self, nodeId=None, nodeName=None):
        neighbors = set()

        if nodeId is not None:
            nodeName = self.entities_id_dict.get(nodeId)

        backNodeSet = self.rt_dict.get(nodeName)
        forwardNodeSet = self.hr_dict.get(nodeName)

        if backNodeSet is not None:
            for node in backNodeSet:
                nNodeName = node[1]
                nNodeId = self.reversed_entities_id_dict.get(nNodeName)
                neighbors.add(nNodeId)

        if forwardNodeSet is not None:
            for node in forwardNodeSet:
                nNodeName = node[0]
                nNodeId = self.reversed_entities_id_dict.get(nNodeName)
                neighbors.add(nNodeId)

        return neighbors

    def getEntitySubgraph(self, nodeIdList, kg):
        nodeList = list(map(self.entities_id_dict.get, nodeIdList))
        hts = set(it.permutations(nodeList, 2))
        for ht in hts:
            tripleSet = set()
            htt = self.htt_set.get(ht)
            if htt:
                for t in htt:
                    newt = (self.reversed_entities_id_dict.get(t[0]), self.reversed_relations_id_dict.get(t[1]),
                            self.reversed_entities_id_dict.get(t[2]))
                    tripleSet.add(newt)

                kg.add_relations(tripleSet)

    def getSubgraph(self, nodeIdList):
        nodeList = list(map(self.entities_id_dict.get, nodeIdList))
        hts = set(it.permutations(nodeList, 2))
        tripleSet = set()
        AtripleSet = set()
        for ht in hts:
            htt = self.htt_set.get(ht, set())
            if htt:
                for t in htt:
                    # newt = (self.reversed_entities_id_dict.get(t[0]), self.reversed_relations_id_dict.get(t[1]),
                    #         self.reversed_entities_id_dict.get(t[2]))
                    newt = (t[0], t[1], t[2])
                    tripleSet.add(newt)

        for node in nodeList:
            hat = self.hat_set.get(node, set())
            if hat:
                for t in hat:
                    # newt = (self.reversed_entities_id_dict.get(t[0]), self.reversed_attributes_id_dict.get(t[1]), t[2])
                    newt = (t[0], t[1], t[2])
                    AtripleSet.add(newt)

        kg = KG(tripleSet, AtripleSet)
        return kg
