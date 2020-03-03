# coding: utf-8
# File: question_parser.py
# Author: houbowen
# Date: 2018-04-10

class QuestionParser:
    '''构建实体节点'''

    def build_entity_dict(self, args):
        entity_dict = {}
        for key, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [key]
                else:
                    entity_dict[type].append(key)

        return entity_dict

    '''解析主函数'''

    def parser_main(self, question_classify):
        args = question_classify['args']
        entity_dict = self.build_entity_dict(args)
        question_types = question_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql = []
            sql1 = []
            sql_['question_type'] = question_type


            # '''查询疾病的原因'''
            if question_type == 'disease_cause':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询疾病的预防措施'''
            elif question_type == 'disease_prevent':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询疾病的周期'''
            elif question_type == 'disease_treatment_cycle':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询疾病的治愈概率'''
            elif question_type == 'disease_cured_rate':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询疾病的治疗方式'''
            elif question_type == 'disease_treatment':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询疾病的易感人群'''
            elif question_type == 'disease_suscep_popu':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询疾病的相关介绍'''
            elif question_type == 'disease_intro':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询疾病有哪些症状'''
            elif question_type == 'disease_symptom':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询症状会导致哪些疾病'''
            elif question_type == 'symptom_disease':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('symptom'))

            # '''查询疾病的并发症'''
            elif question_type == 'disease_complication':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询疾病的禁忌食物'''
            elif question_type == 'disease_not_food':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询疾病建议吃的食物'''
            elif question_type == 'disease_do_food':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''已知禁忌食物查疾病'''
            elif question_type == 'food_not_disease':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('food'))

            # '''已知推荐食物查疾病'''
            elif question_type == 'food_do_disease':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('food'))

            # '''查询疾病常用药品'''
            elif question_type == 'disease_drug':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询已知药品能治疗的疾病'''
            elif question_type == 'drug_disease':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('drug'))

            # '''查询疾病应该进行的检查'''
            elif question_type == 'disease_check':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('disease'))

            # '''查询检查能检查的疾病'''
            elif question_type == 'check_disease':
                sql, sql1 = self.sql_transfer(question_type, entity_dict.get('check'))

            if sql:
                sql_['sql'] = sql
                sql_['sql1'] = sql1

                sqls.append(sql_)

        return sqls

    '''对问句中的每种问题进行处理'''

    def sql_transfer(self, question_type, entities):

        if not entities:
            return []

        '''数据库查询语句'''
        sql = []
        sqql = []
        # '''查询疾病的原因'''
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(item) for item in entities]

        # '''查询疾病的预防措施'''
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(item) for item in entities]

        # '''查询疾病的周期'''
        elif question_type == 'disease_treatment_cycle':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.treatment_cycle".format(item) for item in
                   entities]

        # '''查询疾病的治愈概率'''
        elif question_type == 'disease_cured_rate':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_rate".format(item) for item in
                   entities]

        # '''查询疾病的治疗方式'''
        elif question_type == 'disease_treatment':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.treatment".format(item) for item in
                   entities]

        # '''查询疾病的易感人群'''
        elif question_type == 'disease_suscep_popu':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.suscep_popu".format(item) for item in
                   entities]

        # '''查询疾病的相关介绍'''
        elif question_type == 'disease_intro':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.intro".format(item) for item in entities]

        # '''查询疾病有哪些症状'''
        elif question_type == 'disease_symptom':
            sql = [
                "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]

        # '''查询症状会导致哪些疾病'''
        elif question_type == 'symptom_disease':
            sql = [
                "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]

        # '''查询疾病的并发症'''
        elif question_type == 'disease_complication':
            sql1 = [
                "MATCH (m:Disease)-[r:accompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:accompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]
            sql = sql1+sql2

        # '''查询疾病的禁忌食物'''
        elif question_type == 'disease_not_food':
            sql = ["MATCH (m:Disease)-[r:not_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(
                item) for item in entities]

        # '''查询疾病建议吃的食物'''
        elif question_type == 'disease_do_food':
            sql1 = [
                "MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(item)
                for item in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommend_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]
            sql = sql1+sql2

        # '''已知禁忌食物查疾病'''
        elif question_type == 'food_not_disease':
            sql = ["MATCH (m:Disease)-[r:not_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(
                item) for item in entities]

        # '''已知推荐食物查疾病'''
        elif question_type == 'food_do_disease':
            sql1 = [
                "MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(item)
                for item in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommend_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]
            sql =sql1+sql2

        # '''查询疾病常用药品'''
        elif question_type == 'disease_drug':
            sql1 = [
                "MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommend_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]
            sql =sql1+sql2

        # '''查询已知药品能治疗的疾病'''
        elif question_type == 'drug_disease':
            sql1 = [
                "MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommend_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]
            sql = sql1+sql2

        # '''查询疾病应该进行的检查'''
        elif question_type == 'disease_check':
            sql = [
                "MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]

        # '''查询检查能检查的疾病'''
        elif question_type == 'check_disease':
            sql = [
                "MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}' return m.name, r.name, n.name".format(
                    item) for item in entities]

        if question_type.split('_')[0] == 'disease':
            sqql = [
                "MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause, m.cured_rate, m.intro, m.prevent, m.sick_ratio, m.suscep_popu, m.treatment, m.treatment_cycle, m.visit_department".format(
                    item) for item in entities]

        return sql,sqql


def main():
    handler = QuestionParser()


if __name__ == '__main__':
    main()
