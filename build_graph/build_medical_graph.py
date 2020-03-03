# coding: utf-8
# File: data_spider.py
# Author: houbowen
# Date: 2018-03-30

import os
import json
from py2neo import Graph, Node
import pymongo

class MedicalGraph:

    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn['medical']
        self.data_path = '../data/medical.json'
        self.g = Graph(
            host = 'localhost',
            http_port = '7404',
            user = 'neo4j',
            password = '123456'
        )
        '''节点'''
        self.drugs = set()  # 药品
        self.foods = set()  # 食物
        self.checks = set()  # 检查
        self.departments = set()  # 科室
        self.producers = set()  #生产商
        self.diseases = set()  # 疾病
        self.symptoms = set()  # 症状

        self.disease_infos = []

        '''节点实体关系'''
        self.department_rels = []  # 科室与科室
        self.not_eat_rels = []  # 疾病与禁忌食物
        self.do_eat_rels = []  # 疾病与宜吃食物
        self.recommended_eat_rels = []  # 疾病与推荐食物
        self.common_drug_rels = []  # 疾病与通用药品
        self.recommanded_drug_rels = []  # 疾病与热门药品
        self.check_rels = []  # 疾病与热门药品
        self.drug_producer_rels = []  # 厂商与药物
        self.symptom_rels = []  # 疾病与病症
        self.complication_rels = []  # 并发疾病
        self.category_rels = []  # 疾病与科室


    '''读取文件'''
    def read_nodes(self):


        disease_dict = {}
        count = 0
        for data_json in self.db['data_modify'].find():
            disease_dict = {}
            count += 1
            disease = data_json['name']
            disease_dict['name'] = disease
            self.diseases.add(disease)


            '''疾病的相关属性'''
            disease_dict['intro'] = ''
            disease_dict['prevent'] = ''    #数据库中的相关数据还未修改
            disease_dict['cause'] = ''
            disease_dict['suscep_popu'] = ''
            disease_dict['sick_ratio'] = ''
            disease_dict['visit_department'] = ''   #数据库中的相关数据还未修改
            disease_dict['treatment'] = ''
            disease_dict['treatment_cycle'] = ''
            disease_dict['symptom'] = ''
            disease_dict['cured_rate'] = ''

            if 'symptom' in data_json:
                self.symptoms.update(data_json['symptom'])
                for symptom in data_json['symptom']:
                    self.symptom_rels.append([disease, symptom])

            if 'complication' in data_json:
                for complication in data_json['complication']:
                    self.complication_rels.append([disease, complication])

            if 'intro' in data_json:
                disease_dict['intro'] = data_json['intro']

            if 'prevent' in data_json:
                disease_dict['prevent'] = data_json['prevent']

            if 'cause' in data_json:
                disease_dict['cause'] = data_json['cause']

            if 'suscep_popu' in data_json:
                disease_dict['suscep_popu'] = data_json['suscep_popu']

            if 'sick_ratio' in data_json:
                disease_dict['sick_ratio'] = data_json['sick_ratio']

            if 'visit_department' in data_json:
                department = data_json['visit_department']
                if len(department) == 1:
                    self.category_rels.append([disease, department[0]])
                if len(department) == 2:
                    big = department[0]
                    small = department[1]
                    self.department_rels.append([big, small])
                    self.category_rels.append([disease, small])

                disease_dict['visit_department'] = department
                self.departments.update(department)

            if 'treatment' in data_json:
                disease_dict['treatment'] = data_json['treatment']

            if 'treatment_cycle' in data_json:
                disease_dict['treatment_cycle'] = data_json['treatment_cycle']

            if 'cured_rate' in data_json:
                disease_dict['cured_rate'] = data_json['cured_rate']

            if 'common_drug' in data_json:
                common_drug = data_json['common_drug']
                for drug in common_drug:
                    self.common_drug_rels.append([disease, drug])
                self.drugs.update(common_drug)

            if 'recommend_drug' in data_json:   #需要修改
                recommended_drug = data_json['recommend_drug']
                for drug in recommended_drug:
                    self.recommanded_drug_rels.append([disease, drug])
                self.drugs.update(recommended_drug)

            if 'not_eat' in data_json:
                not_eat = data_json['not_eat']
                self.foods.update(not_eat)
                for not_ in not_eat:
                    self.not_eat_rels.append([disease, not_])

                do_eat = data_json['do_eat']
                self.foods.update(do_eat)
                for do_ in do_eat:
                    self.do_eat_rels.append([disease, do_])

                recommended_eat = data_json['recommend_food'] #需要修改
                self.foods.update(recommended_eat)
                for recommended_ in recommended_eat:
                    self.recommended_eat_rels.append([disease, recommended_])

            if 'check' in data_json:
                check = data_json['check']
                self.checks.update(check)

                for check_ in check:
                    self.check_rels.append([disease, check_])

            if 'drug_details' in data_json:
                drug_details = data_json['drug_details']

                for drug_detail in drug_details:
                    producer = drug_detail.split()[0]
                    drug = drug_detail.split('(')[-1].replace(')', '')
                    self.drug_producer_rels.append([producer, drug])
                    self.producers.add(producer)
            self.disease_infos.append(disease_dict)
       # print(self.drugs,self.diseases,self.departments,self.symptoms,self.foods,self.producers,self.checks)

    '''建立节点'''
    def create_node(self, nodes, label):
        count = 0
        for node_name in nodes:
            node =Node(label, name = node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中间节点'''
    def create_diseases_node(self, diseases_info):
        count = 0
        for disease_dict in diseases_info:
            node = Node("Disease", name = disease_dict['name'], intro = disease_dict['intro'],
                        prevent = disease_dict['prevent'], cause = disease_dict['cause'],
                        suscep_popu = disease_dict['suscep_popu'], treatment_cycle = disease_dict['treatment_cycle'],
                        visit_department = disease_dict['visit_department'], treatment = disease_dict['treatment'],
                        cured_rate = disease_dict['cured_rate'], sick_ratio = disease_dict['sick_ratio'])
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型'''
    def create_entity_nodes(self):
        self.create_diseases_node(self.disease_infos)
        self.create_node(self.drugs, 'Drug')
        self.create_node(self.foods, 'Food')
        self.create_node(self.checks, 'Check')
        self.create_node(self.departments, 'Department')
        self.create_node(self.producers, 'Producer')
        self.create_node(self.symptoms, 'Symptom')

        return

    '''创建实体关联边''' ## 需要理解
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''创建知识图谱实体关联边'''
    def create_graph_relationships(self):
        self.create_relationship('Disease', 'Food', self.recommended_eat_rels, 'recommend_eat', '推荐食谱')
        self.create_relationship('Disease', 'Food', self.not_eat_rels, 'not_eat', '忌食')
        self.create_relationship('Disease', 'Food', self.recommended_eat_rels, 'do_eat', '宜吃')
        self.create_relationship('Department', 'Department', self.department_rels, 'belong_to', '属于')
        self.create_relationship('Disease', 'Drug', self.common_drug_rels, 'common_drug', '常用药品')
        self.create_relationship('Producer', 'Drug', self.drug_producer_rels, 'drug_of', '生产药品')
        self.create_relationship('Disease', 'Drug', self.recommanded_drug_rels, 'recommend_drug', '推荐药品')
        self.create_relationship('Disease', 'Check', self.check_rels, 'need_check', '诊断检查')
        self.create_relationship('Disease', 'Symptom', self.symptom_rels, 'has_symptom', '症状')
        self.create_relationship('Disease', 'Disease', self.complication_rels, 'accompany_with', '并发症')
        self.create_relationship('Disease', 'Department', self.category_rels, 'belong_to', '所属科室')

    def export_data(self):
        f_drug = open('../dict/drug.txt', 'w+', encoding='utf-8')
        f_food = open('../dict/food.txt', 'w+', encoding='utf-8')
        f_check = open('../dict/check.txt', 'w+', encoding='utf-8')
        f_department = open('../dict/department.txt', 'w+', encoding='utf-8')
        f_producer = open('../dict/producer.txt', 'w+', encoding='utf-8')
        f_symptom = open('../dict/symptoms.txt', 'w+', encoding='utf-8')

        f_drug.write('\n'.join(list(self.drugs)))
        f_food.write('\n'.join(list(self.foods)))
        f_check.write('\n'.join(list(self.checks)))
        f_department.write('\n'.join(list(self.departments)))
        f_producer.write('\n'.join(list(self.producers)))
        f_symptom.write('\n'.join(list(self.symptoms)))

        f_drug.close()
        f_food.close()
        f_check.close()
        f_department.close()
        f_producer.close()
        f_symptom.close()

def main():
    medical_graph = MedicalGraph()
    medical_graph.read_nodes()
    # medical_graph.create_entity_nodes()
    # medical_graph.create_graph_relationships()
    medical_graph.export_data()

if __name__ == '__main__':
    main()
