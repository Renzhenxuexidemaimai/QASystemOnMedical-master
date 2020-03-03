# !/usr/bin/env python3
# coding: utf-8
# File: data_spider.py
# Author: houbowen
# Date: 2018-03-27

import requests
from bs4 import BeautifulSoup
import lxml
from pymongo import MongoClient
from requests.exceptions import RequestException
import re
from config.config import *
from multiprocessing.pool import Pool
import multiprocessing

'''寻医问药网医疗数据爬取'''

'''由url请求网页信息'''

conn = MongoClient(MONGO_CLIENT_URL, MONGO_CLIENT_PORT)
db = conn['medical']
col = db['data']

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/72.0.3626.121 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'gb2312'
        if (response.status_code == 200):
            return response.text
        else:
            print('获取网页失败', url)
            return None
    except RequestException as e:
        print(e, '获取网页失败', url)
        return None


'''主要信息抓取模块'''


def main_crawl(page):
    try:
        data = {}
        data['url'] = URL['basic_url'] % page
        data['basic_info'] = basic_spider(URL['basic_url'] % page)
        data['treat_info'] = treat_spider(URL['treat_url'] % page)
        data['drug_info'] = drug_spider(URL['drug_url'] % page)
        data['food_info'] = food_spider(URL['food_url'] % page)
        data['symptom_info'] = symptom_spider(URL['symptom_url'] % page)
        data['inspect_info'] = inspect_spider(URL['inspect_url'] % page)
        data['prevent_info'] = prevent_spider(URL['prevent_url'] % page)
        data['cause_info'] = cause_spider(URL['cause_url'] % page)
        col.insert(data)
        # print(data['url'])
    except Exception as e:
        print(e, page)


'''爬取疾病基本信息'''


def basic_spider(url):
    html = get_html(url)

    try:
        soup = BeautifulSoup(html, 'lxml')
        title = soup.select('body > div.wrap.mt5 > div')[0].get_text().strip()
        titel = title.replace('\r', '').replace('\n', '').replace('\xa0', '')
        category = soup.select('body > div.wrap.mt10.nav-bar')[0].get_text().strip()
        category = category.replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace('\t', '')
        intro = soup.select('body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl '
                            '> div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div'
                            '.jib-articl-con.jib-lh-articl > p')
        intro = [p.get_text() for p in intro]
        ps = soup.select('body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > '
                         'div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > '
                         'div.mt20.articl-know > p')
        info_col = []

        for p in ps:
            info = p.get_text().strip()
            info = info.replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace('\t', '')
            info_col.append(info)

        basic_data = {}
        basic_data['title'] = title
        basic_data['category'] = category
        basic_data['intro'] = intro
        basic_data['attributes'] = info_col
        if (title is not ""):
            print(title)
            with open('../dict/disease.txt', 'a', encoding='utf-8') as f:
                f.write(title + '\n')
        return basic_data
    except Exception as e:
        print(e, url, '爬取基本信息出错')
        return None


'''爬取治疗信息'''


def treat_spider(url):
    html = get_html(url)
    try:
        soup = BeautifulSoup(html, 'lxml')
        ps = soup.select('body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl >'
                         ' div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div.mt20.'
                         'articl-know > p')

        info_col = []

        for p in ps:
            info = p.get_text().strip()
            info = info.replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace('\t', '')
            info_col.append(info)

        return info_col
    except Exception as e:
        print(e, url, '爬取治疗信息出错')
        return None


'''爬取药物治疗信息'''


def drug_spider(url):
    html = get_html(url)

    try:
        soup = BeautifulSoup(html, 'lxml')
        drugs = []
        ps = soup.select('body > div.wrap.mt10.clearfix.graydeep > '
                         'div.main-sub.fl > div > div > div > div'
                         ' > div.fl.drug-pic-rec.mr30')
        for p in ps:
            info = p.p.a.get_text().strip()
            info = info.replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace('\t', '')
            drugs.append(info)

        return drugs
    except Exception as e:
        print(e, url, '爬取药物治疗信息出错')
        return None


'''爬取食物治疗信息'''


def food_spider(url):
    html = get_html(url)
    foods = {}

    try:
        soup = BeautifulSoup(html, 'lxml')
        ps = soup.select('body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > '
                         'div.jib-janj.bor.clearfix > div.jib-articl.fr.f14.jib-lh-articl '
                         '> div > div.panels.mt10 > div.diet-item.none '
                         '> div.diet-img.clearfix.mt20')

        good_info = ps[0].select('div > p')
        bad_info = ps[1].select('div > p')
        recommand_info = ps[2].select('div > p')
        foods['good'] = [info.get_text().strip() for info in good_info]
        foods['bad'] = [info.get_text().strip() for info in bad_info]
        foods['recomand'] = [info.get_text().strip() for info in recommand_info]

        return foods
    except Exception as e:
        # print(e, url, '爬取食物资料信息失败')
        return {}


'''爬取症状信息'''


def symptom_spider(url):
    html = get_html(url)

    try:
        soup = BeautifulSoup(html, 'lxml')
        symptom_info = soup.select('body > div.wrap.mt10.clearfix.graydeep > '
                                   'div.main-sub.fl > div.jib-janj.bor.clearfix > '
                                   'div.jib-articl.fr.f14.jib-lh-articl > span > a')
        symptoms = [info.get_text() for info in symptom_info]

        details = []
        detail_info = soup.select('body > div.wrap.mt10.clearfix.graydeep > '
                                  'div.main-sub.fl > div.jib-janj.bor.clearfix'
                                  ' > div.jib-articl.fr.f14.jib-lh-articl > p')
        for info in detail_info:
            info = info.get_text().strip()
            info = info.replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace('\t', '')
            details.append(info)

        symptoms_data = {}
        symptoms_data['symptom'] = symptoms
        symptoms_data['details'] = details

        return symptoms_data
    except Exception as e:
        print(e, url, '爬取症状信息失败')
        return None


'''爬取检查信息'''


def inspect_spider(url):
    html = get_html(url)

    try:
        soup = BeautifulSoup(html, 'lxml')
        inspect_info = soup.select(
            'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14.jib-lh-articl > div > ul > li.check-item > a.gre')
        inspects = []

        for info in inspect_info:
            inspect = info.attrs.get('href', 'default')
            inspects.append(inspect)

        return inspects
    except Exception as e:
        print(e, url, '爬取检查信息失败')
        return None


'''爬取预防信息'''


def prevent_spider(url):
    html = get_html(url)

    try:
        soup = BeautifulSoup(html, 'lxml')
        ps = soup.select('body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl'
                         ' > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14.jib'
                         '-lh-articl > p')
        prevent_info = []
        for p in ps:
            info = p.get_text().strip()
            info = info.replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace('\t', '')
            if info:
                prevent_info.append(info)
        return '\n'.join(prevent_info)
    except Exception as e:
        print(e, url, '爬取预防信息失败')
        return None


'''爬取病因信息'''


def cause_spider(url):
    html = get_html(url)

    try:
        soup = BeautifulSoup(html, 'lxml')
        ps = soup.select('body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl'
                         ' > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14.jib'
                         '-lh-articl > p')
        cause_info = []
        for p in ps:
            info = p.get_text().strip()
            info = info.replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace('\t', '')
            if info:
                cause_info.append(info)
        return '\n'.join(cause_info)

    except Exception as e:
        print(e, url, '爬取病因信息失败')
        return None


'''检查项信息抓取模块'''


def inspect_crawl(page):
    url = ''
    try:
        url = URL['inspect'] % page
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        data = {}
        data['url'] = url
        data['html'] = html
        db['jc'].insert(data)
        print(url)
    except Exception as e:
        print(e, url, '爬取检查模块失败')


def main():
    pool = Pool(multiprocessing.cpu_count())

    # pool.map(main_crawl, [i for i in range(1, TOTAL_PAGE)])
    #
    # pool.close()
    # pool.join()

    # pool.map(inspect_crawl, [i for i in range(1, INSPECT_TOTAL_PAGE)])
    #
    # pool.close()
    # pool.join()


if __name__ == '__main__':
    main()
