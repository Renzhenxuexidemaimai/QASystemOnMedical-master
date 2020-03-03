# coding: utf-8
# File: question_classifier.py
# Author: houbowen
# Date: 2018-04-09

import ahocorasick
import os


class QuestionClassifier:

    def __init__(self):

        '''加载特征值'''
        path = os.getcwd().split('\\')[:-1]
        path = '/'.join(path)+'/'
        self.disease_wds = [item.strip() for item in open('dict/disease.txt', encoding='utf-8') if item.strip()]
        self.department_wds = [item.strip() for item in open('dict/department.txt', encoding='utf-8') if
                               item.strip()]
        self.check_wds = [item.strip() for item in open('dict/check.txt', encoding='utf-8') if item.strip()]
        self.food_wds = [item.strip() for item in open('dict/food.txt', encoding='utf-8') if item.strip()]
        self.drug_wds = [item.strip() for item in open('dict/drug.txt', encoding='utf-8') if item.strip()]
        self.producer_wds = [item.strip() for item in open('dict/producer.txt', encoding='utf-8') if item.strip()]
        self.symptom_wds = [item.strip() for item in open('dict/symptoms.txt', encoding='utf-8') if item.strip()]
        self.deny_wds = [item.strip() for item in open('dict/deny.txt', encoding='utf-8') if item.strip()]
        self.region_wds = set(self.disease_wds + self.department_wds + self.check_wds + self.food_wds \
                              + self.drug_wds + self.producer_wds + self.symptom_wds)
        '''构造领域atree'''
        self.region_tree = self.build_actree(list(self.region_wds))

        '''构造词对应的类型'''
        self.region_dict = self.build_wdtype_dict()

        '''问句疑问词'''
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现', '征兆', '病症']
        self.cause_qwds = ['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致',
                           '会造成', '病因', '病因', '发病原因', '导致', '如何产生','怎样产生']
        self.complication_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜', '忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物', '补品']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.treatment_cycle_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.treatment_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治','治疗方式']
        self.cured_rate_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医']
        self.suscep_popu_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上','容易得']
        self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要', '有帮助', '有啥好处']

    '''构造atree'''

    def build_actree(self, worllist):
        actree = ahocorasick.Automaton()
        for idx, key in enumerate(worllist):
            actree.add_word(key, (idx, key))
        actree.make_automaton()
        return actree

    '''构造词对应的类型'''

    def build_wdtype_dict(self):
        wd_dict = dict()

        for wd in self.region_wds:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.check_wds:
                wd_dict[wd].append('check')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.producer_wds:
                wd_dict[wd].append('producer')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
        return wd_dict

    '''问句过滤'''

    def parse_question(self, question):
        question_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            question_wds.append(wd)
        stop_wds = []
        for wd1 in question_wds:
            for wd2 in question_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in question_wds if i not in stop_wds]
        final_dict = {i: self.region_dict.get(i) for i in final_wds}

        return final_dict

    def check_words(self, wds, question):
        for wd in wds:
            if wd in question:
                return True
        return False

    '''疾病分类'''

    def classify(self, question):
        data = {}
        entity_dict = self.parse_question(question)
        if not entity_dict:
            return {}

        entity_types = []
        for type_ in entity_dict.values():
            entity_types += type_

        data['args'] = entity_dict
        question_types = []

        '''疾病推症状'''
        if self.check_words(self.symptom_qwds, question) and ('disease' in entity_types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        '''症状推疾病'''
        if self.check_words(self.symptom_qwds, question) and ('symptom' in entity_types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        '''疾病原因'''
        if self.check_words(self.cause_qwds, question) and ('disease' in entity_types):
            question_type = 'disease_cause'
            question_types.append(question_type)

        '''疾病并发症'''
        if self.check_words(self.complication_qwds, question) and ('disease' in entity_types):
            question_type = 'disease_complication'
            question_types.append(question_type)

        '''推荐食物'''
        if self.check_words(self.food_qwds, question) and ('disease' in entity_types):
            if self.check_words(self.deny_wds, question):
                question_type = 'disease_not_food'
            else:
                question_type = 'disease_do_food'
            question_types.append(question_type)

        '''食物推疾病'''
        if self.check_words(self.food_qwds + self.cure_qwds, question) and ('food' in entity_types):
            if self.check_words(self.deny_wds, question):
                question_type = 'food_not_disease'
            else:
                question_type = 'food_do_disease'
            question_types.append(question_type)

        '''疾病推荐药物'''
        if self.check_words(self.drug_wds, question) and ('disease' in entity_types):
            question_type = 'disease_drug'
            question_types.append(question_type)

        '''药物能治啥病'''
        if self.check_words(self.cure_qwds, question) and ('drug' in entity_types):
            question_type = 'drug_disease'
            question_types.append(question_type)

        '''疾病的检查项目'''
        if self.check_words(self.check_qwds, question) and ('disease' in entity_types):
            question_type = 'disease_check'
            question_types.append(question_type)

        '''已知检查项目能检查出哪些疾病'''
        if self.check_words(self.check_qwds + self.cure_qwds, question) and ('check' in entity_types):
            question_type = 'check_disease'
            question_types.append(question_type)

        '''疾病预防'''
        if self.check_words(self.prevent_qwds, question) and ('disease' in entity_types):
            question_type = 'disease_prevent'
            question_types.append(question_type)

        '''疾病的治疗周期'''
        if self.check_words(self.treatment_cycle_qwds, question) and ('disease' in entity_types):
            question_type = 'disease_treatment_cycle'
            question_types.append(question_type)

        '''疾病的治疗方式'''
        if self.check_words(self.treatment_qwds, question) and ('disease' in entity_types):
            question_type = 'disease_treatment'
            question_types.append(question_type)

        '''疾病的治愈可能性'''
        if self.check_words(self.cured_rate_qwds, question) and ('disease' in entity_types):
            question_type = 'disease_cured_rate'
            question_types.append(question_type)

        '''疾病易感人群'''
        if self.check_words(self.suscep_popu_qwds, question) and ('disease' in entity_types):
            question_type = 'disease_suscep_popu'
            question_types.append(question_type)

        '''如果没有查到相关查询信息，但是有疾病信息，将相关疾病信息返回'''
        if question_types == [] and 'disease' in entity_types:
            question_types = ['disease_intro']

        '''如果没有查到相关查询信息，但是有症状信息，将相关疾病信息返回'''
        if question_types == [] and 'symptom' in entity_types:
            question_types = ['symptom_disease']

        data['question_types'] = question_types
        return data


def main():
    question = '什么人容易得高血压'
    handler = QuestionClassifier()
    handler.classify(question)


if __name__ == '__main__':
    main()
