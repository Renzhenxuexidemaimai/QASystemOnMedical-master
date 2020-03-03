# coding: utf-8
# File: data_spider.py
# Author: houbowen
# Date: 2018-03-27

MONGO_CLIENT_URL = 'localhost'
MONGO_CLIENT_PORT = 27017

TOTAL_PAGE = 10139

INSPECT_TOTAL_PAGE = 3683

URL = {
    'basic_url': 'http://jib.xywy.com/il_sii/gaishu/%s.htm',
    'cause_url': 'http://jib.xywy.com/il_sii/cause/%s.htm',
    'prevent_url': 'http://jib.xywy.com/il_sii/prevent/%s.htm',
    'symptom_url': 'http://jib.xywy.com/il_sii/symptom/%s.htm',
    'inspect_url': 'http://jib.xywy.com/il_sii/inspect/%s.htm',
    'treat_url': 'http://jib.xywy.com/il_sii/treat/%s.htm',
    'food_url': 'http://jib.xywy.com/il_sii/food/%s.htm',
    'drug_url': 'http://jib.xywy.com/il_sii/drug/%s.htm',
    'inspect': 'http://jck.xywy.com/jc_%s.html',
}