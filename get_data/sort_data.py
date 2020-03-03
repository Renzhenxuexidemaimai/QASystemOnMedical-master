# !/usr/bin/env python3
# coding: utf-8
# File: sort_data.py
# Author: houbowen
# Date: 2018-03-28

from pymongo import MongoClient
from bs4 import BeautifulSoup
import lxml
import os
import json
import chardet
from bson import json_util
from get_data.segment_data import *
from config.config import *

class MedicalGraph:

    def __init__(self):
        self.conn = MongoClient(MONGO_CLIENT_URL, MONGO_CLIENT_PORT)
        self.db = self.conn['medical']
        self.col = self.db['data']
        f = open('../dict/first_name.txt', 'r', encoding='utf-8')
        first_names = f.read().split()
        f.close()
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y', 'z']
        self.forbid_words = nums + alphabets + first_names
        self.key_dict = {
            '医保疾病' : 'med_insurance_status',
            "患病比例" : "sick_ratio",
            "易感人群" : "suscep_popu",
            "传染方式" : "infect_mode",
            "就诊科室" : "visit_department",
            "治疗方式" : "treatment",
            "治疗周期" : "treatment_cycle",
            "治愈率" : "cured_rate",
            '药品明细': 'drug_details',
            '药品推荐': 'recommend_drug',
            '推荐': 'recommend_food',
            '忌食': 'not_eat',
            '宜食': 'do_eat',
            '症状': 'symptom',
            '检查': 'check',
            '成因': 'cause',
            '预防措施': 'prevent',
            '所属类别': 'category',
            '简介': 'intro',
            '名称': 'name',
            '常用药品' : 'common_drug',
            '治疗费用': 'treatment_cost',
            '并发症': 'complication'
        }
        self.segment = Segment()

    def sort_medical_data(self):
        count = 0

        for item in self.col.find():
            try:

                data = {}
                basic_info = item['basic_info']
                name = basic_info['title']
                if name is '':
                    continue

                '''基本信息'''
                data['名称'] = name
                data['简介'] = '\n'.join(basic_info['intro']).replace('\r\n\t','').replace('\r\n\n\n','').replace(' ','').replace('\r\n','\n')
                category = basic_info['category'].split('>')[1:-1]
                data['所属类别'] = category
                inspect = item['inspect_info']

                '''疾病原因以及预防'''
                data['预防措施'] = item['prevent_info']
                data['成因'] = item['cause_info']

                '''并发症'''
                symptoms = item['symptom_info']['symptom']
                data['症状'] = list(set([symptom for symptom in symptoms if symptom[0] not in self.forbid_words]))

                '''其它属性'''
                attributes = basic_info['attributes']
                for attr in attributes:
                    attr_pair = attr.split('：')
                    if(len(attr_pair) == 2):
                        data[attr_pair[0]] = attr_pair[1]

                '''检查'''
                inspects = item['inspect_info']
                inspect_names = []
                for inspect in inspects:
                    inspect_name = self.get_inspect_name(inspect)
                    inspect_names.append(inspect_name)
                data['检查'] = inspect_names

                '''食物'''
                food_info = item['food_info']
                if food_info:
                    data['宜食'] = food_info['good']
                    data['忌食'] = food_info['bad']
                    data['推荐'] = food_info['recomand']

                '''药品'''
                drug_info = item['drug_info']
                data['药品推荐'] = list(set([item.split('(')[-1].replace(')','') for item in drug_info]))
                data['药品明细'] = drug_info

                '''数据修改'''
                data_modify = {}
                for attr, value in data.items():
                    attr_en =self.key_dict.get(attr)
                    need_modify_attr1 = ['med_insurance_status', 'sick_ratio', 'suscep_popu', 'infect_mode', 'treatment_cycle', 'cured_rate']
                    need_modify_attr2 = ['treatment', 'visit_department', 'common_drug']
                    if attr_en:
                        data_modify[attr_en] = value
                    if attr_en in need_modify_attr1:
                        data_modify[attr_en] = value.replace(' ','').replace('\t','')
                    if attr_en in need_modify_attr2:
                        data_modify[attr_en] = [item for item in value.split()]
                    if attr_en in ['complication']:
                        complication = [item for item in self.segment.maximum_biward_match(data_modify[attr_en]) if len(item) > 1]
                        data_modify[attr_en] = complication
                self.db['data_modify'].insert(data_modify)
                count += 1
                print(count)
            except Exception as e:
                print(e)

    def get_inspect_name(self, url):
        data = self.db['jc'].find_one({'url':url})
        if not data:
            return ''
        else:
            return data['name']

    def modify_jc(self):
        for item in self.db['jc'].find():
            try:
                url = item['url']
                html = item['html']
                soup = BeautifulSoup(html, 'lxml')
                name = soup.select('title')[0].get_text().split('结果分析')[0]
                intro = soup.select('head > meta:nth-child(6)')[0].attrs.get('content', 'default').strip().replace('\r\n\t', '')
                self.db['jc'].update({'url': url}, {'$set':{'name': name, 'intro': intro}})
            except Exception as e:
                print(e)

    def export_to_file(self):
        count = 1
        for item in self.db['data_modify'].find():
            # str = list(item.values())[2]
            # print(chardet.detect(str))
            item_json = json.dumps(item, default= json_util.default, ensure_ascii= False)

            with open('../data/medical.json', 'a', encoding= 'utf-8') as f:
                json.dump(item_json, f)

            for data in open('../data/medical.json', encoding= 'utf-8'):
                print(data)
def main():
    graph = MedicalGraph()
    graph.sort_medical_data()
    # graph.export_to_file()

if __name__ == '__main__':
    main()