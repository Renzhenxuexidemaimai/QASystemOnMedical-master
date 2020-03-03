# coding: utf-8
# File: question_answer.py
# Author: houbowen
# Date: 2018-04-10

from QASystem.question_classifier import *
from QASystem.question_parser import *
from QASystem.answer_search import *

class QuestionAnswer:

    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionParser()
        self.searcher = AnswerSearch()

    def answer_main(self, question):
        answer = '您好，我是小博智能医药助理，希望可以帮到您。'
        classifier  = self.classifier.classify(question)
        print('classifier'+str(classifier))
        if not classifier:
            return answer,False,None

        sqls = self.parser.parser_main(classifier)
        print('sqls'+str(sqls))
        final_answers, final_answers1 = self.searcher.search_main(sqls)
        print('final_answers'+str(final_answers))
        if not final_answers:
            return answer, final_answers1, False,None
        else:
            return '\r\n'.join(final_answers), final_answers1, True, classifier['question_types'][0].split('_')[0]


def main():
    handler = QuestionAnswer()
    question = ''
    while question != '再见':
        question = input('用户：')
        answer = handler.answer_main(question)
        print('小博：',answer)

if __name__ == '__main__':
    main()
