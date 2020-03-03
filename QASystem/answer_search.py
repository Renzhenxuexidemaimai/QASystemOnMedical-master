# coding: utf-8
# File: answer_search.py
# Author: houbowen
# Date: 2018-04-10

from py2neo import Graph


class AnswerSearch:

    def __init__(self):
        self.g = Graph(
            host='localhost',
            http_port='7404',
            user='neo4j',
            password='123456'
        )
        self.num_limit = 20

    '''执行cypher查询,并返回相应结果'''

    def search_main(self, sqls):
        final_answers = []
        final_answers1 = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            queries1 = sql_['sql1']
            answers = []
            answers1 = []
            for query in queries:
                res = self.g.run(query).data()
                answers += res
            for query in queries1:
                res = self.g.run(query).data()
                answers1 += res
            final_answer = self.answer_prettify(question_type, answers)
            final_answer1 = self.answer_prettify1(answers1)
            if final_answer:
                final_answers.append(final_answer)
            if final_answer1:
                final_answers1.append(final_answer1)
        return final_answers, final_answers1

    '''根据对应的问题类型，调用相应的回复模板'''

    def answer_prettify1(self, answers):
        final_answers = []
        if not answers:
            return ''

        final_answer = '让我们一起来了解一下{0}吧!以下是关于{0}的相关信息:'.format(answers[0]['m.name'])
        final_answers.append(final_answer)

        final_answer = '名称：{0}'.format(answers[0]['m.name'])
        final_answers.append(final_answer)

        final_answer = '所属科室：{0}'.format(answers[0]['m.visit_department'])
        final_answers.append(final_answer)

        final_answer = '简介：{0}'.format(answers[0]['m.intro'])
        final_answers.append(final_answer)

        final_answer = '发病原因：{0}'.format(answers[0]['m.cause'])
        final_answers.append(final_answer)

        final_answer = '如何预防：{0}'.format(answers[0]['m.prevent'])
        final_answers.append(final_answer)

        final_answer = '发病率：{0}'.format(answers[0]['m.sick_ratio'])
        final_answers.append(final_answer)

        final_answer = '治愈率：{0}'.format(answers[0]['m.cured_rate'])
        final_answers.append(final_answer)

        final_answer = '治疗方法：{0}'.format(answers[0]['m.treatment'])
        final_answers.append(final_answer)

        final_answer = '易感人群：{0}'.format(answers[0]['m.suscep_popu'])
        final_answers.append(final_answer)

        final_answer = '治疗周期：{0}'.format(answers[0]['m.treatment_cycle'])
        final_answers.append(final_answer)

        final_answers = '\r\n'.join(final_answers)

        return final_answers
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''

        if question_type == 'disease_symptom':
            key = [i['n.name'] for i in answers]
            value = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            key = [i['m.name'] for i in answers]
            value = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'disease_cause':
            key = [i['m.cause'] for i in answers]
            value = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            key = [i['m.prevent'] for i in answers]
            value = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'disease_treatment_cycle':
            key = [i['m.treatment_cycle'] for i in answers]
            value = answers[0]['m.name']
            final_answer = '{0}治疗可能持续的周期为：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'disease_treatment':
            key = [';'.join(i['m.treatment']) for i in answers]
            value = answers[0]['m.name']
            final_answer = '{0}可以尝试如下治疗：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'disease_cured_rate':
            key = [i['m.cured_rate'] for i in answers]
            value = answers[0]['m.name']
            final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'disease_suscep_popu':
            key = [i['m.suscep_popu'] for i in answers]
            value = answers[0]['m.name']

            final_answer = '{0}的易感人群包括：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'disease_intro':
            key = [i['m.intro'] for i in answers]
            value = answers[0]['m.name']
            final_answer = '{0},熟悉一下：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'disease_complication':
            key1 = [i['n.name'] for i in answers]
            key2 = [i['m.name'] for i in answers]
            value = answers[0]['m.name']
            key = [i for i in key1 + key2 if i != value]
            final_answer = '{0}的并发症包括：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'disease_not_food':
            key = [i['n.name'] for i in answers]
            value = answers[0]['m.name']
            final_answer = '{0}忌食的食物包括有：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'disease_do_food':
            do_key = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
            recommand_key = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
            value = answers[0]['m.name']
            final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(value, ';'.join(list(set(do_key))[:self.num_limit]),
                                                                 ';'.join(list(set(recommand_key))[:self.num_limit]))

        elif question_type == 'food_not_disease':
            key = [i['m.name'] for i in answers]
            value = answers[0]['n.name']
            final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(key))[:self.num_limit]), value)

        elif question_type == 'food_do_disease':
            key = [i['m.name'] for i in answers]
            value = answers[0]['n.name']
            final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(key))[:self.num_limit]), value)

        elif question_type == 'disease_drug':
            key = [i['n.name'] for i in answers]
            value = answers[0]['m.name']
            final_answer = '{0}通常的使用的药品包括：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'drug_disease':
            key = [i['m.name'] for i in answers]
            value = answers[0]['n.name']
            final_answer = '{0}主治的疾病有{1},可以试试'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'disease_check':
            key = [i['n.name'] for i in answers]
            value = answers[0]['m.name']
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        elif question_type == 'check_disease':
            key = [i['m.name'] for i in answers]
            value = answers[0]['n.name']
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(value, '；'.join(list(set(key))[:self.num_limit]))

        return final_answer


def main():
    handler = AnswerSearch()


if __name__ == '__main__':
    main()
