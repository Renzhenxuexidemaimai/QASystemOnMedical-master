import time
import math
import pymongo
from flask import Flask, render_template, request
from bson.objectid import ObjectId
import json

from pymongo import MongoClient
import paginate

from QASystem import question_answer
from config.config import *

def Paginate(records, per_page, cur_page):
    total = len(records)
    pages = math.ceil(total/per_page)
    has_prevent=has_next = True
    if cur_page == pages:
        has_next = False
    if cur_page == 1:
        has_prevent = False


    begin = 0
    end = 0
    if cur_page == pages:
        begin = (cur_page-1)*per_page
        end = total

    else:
        begin = (cur_page-1)*per_page
        end = begin+per_page

    record = records[begin:end]

    pagination = {'total':total,'per_page':per_page, 'pages':pages, 'has_prevent':has_prevent, 'has_next':has_next,
                  'cur_page': cur_page, 'record':record, 'begin':begin, 'end': end}

    return pagination

conn = MongoClient(MONGO_CLIENT_URL, MONGO_CLIENT_PORT)
db = conn['log']
col = db['logs']

app = Flask(__name__)
handler = question_answer.QuestionAnswer()

@app.route('/index/<question>',methods=["GET", "POST"])
@app.route('/index',methods=["GET", "POST"])
@app.route('/',methods=["GET", "POST"])
def get_index(question=None):
    print(1)
    if  request.method == "GET":
        record = col.find(limit=8, sort=[("_id", pymongo.DESCENDING)])
        records = []
        for r in record:
            records.append(r)
        return render_template('index.html', records=records)
    else:
        answer, answer1, flag, question_type = handler.answer_main(question)
        data = ''
        print(answer1)
        if flag:
            cur_time = time.strftime('%Y.%m.%d',time.localtime(time.time()))
            record = {'question':question, 'answer':answer, 'question_type':question_type,'time':cur_time}
            col.insert(record)
            dic = {'answer':answer,'answer1':answer1}
            data = json.dumps(dic)
        return data

@app.route('/Reply', methods = ["GET", "POST"])
@app.route('/Reply_<int:page_num>',methods=["GET", "POST"])
def get_Reply(page_num=1):
    disease_num = col.count({'question_type':'disease'})
    symptom_num = col.count({'question_type':'symptom'})
    food_num = col.count({'question_type':'food'})
    drug_num = col.count({'question_type':'drug'})
    check_num = col.count({'question_type':'check'})
    record = col.find(sort=[("_id", pymongo.DESCENDING)])
    records = []
    for r in record:
        records.append(r)
    #分页
    pagination = Paginate(records, 8, page_num)
    record = pagination['record']
    return render_template('Reply.html',disease_num=disease_num,symptom_num=symptom_num,food_num=food_num,
                           check_num=check_num, drug_num=drug_num, records=record, pagination=pagination)

@app.route('/ReplyDetail',methods=["GET", "POST"])
@app.route('/ReplyDetail_<_id>',methods=["GET", "POST"])
def get_ReplyDetail(_id):
    print(_id)
    result = col.find({'_id': ObjectId(_id)})
    record = {}
    for re in result:
        record = re
    return render_template('ReplyDetail.html', result=record)

@app.route('/ReplyList',methods=["GET", "POST"])
@app.route('/ReplyList_<category>',methods=["GET", "POST"])
@app.route('/ReplyList_<category>_<int:cur_page>',methods=["GET", "POST"])
def get_ReplyList(category=None, cur_page = 1):
    record = col.find({'question_type': category}, sort=[("_id", pymongo.DESCENDING)])
    records = []
    for re in record:
        records.append(re)
    pagination = Paginate(records, 8, cur_page)
    record = pagination['record']
    question_type = category
    return render_template('ReplyList.html',records=record, pagination=pagination, category=question_type)


if __name__ == '__main__':
    app.run(debug=True)