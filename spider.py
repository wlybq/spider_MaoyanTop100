#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import RequestException
import re
import pymysql
from multiprocessing import Pool


def get_url_content(url):

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):

    re_str_list = '<dd>.*?<i.*?board-index.*?>(\d*?)</i>.*?<a.*?href="(.*?)".*?title="(.*?)".*?<img.*?data-src="(.*?)".*?</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>'
    pattern = re.compile(re_str_list, re.S)
    result = re.findall(pattern, html)
    for item in result:
        yield {
            'id': item[0],
            'url': item[1],
            'title': item[2],
            'image': item[3],
            'actor': item[4].strip()[3:],
            'time': item[5].strip()[5:],
            'score': item[6] + item[7]
        }


def main(i):

    url = 'http://maoyan.com/board/4?offset=%d' % (i * 10)
    html = get_url_content(url)
    result = parse_one_page(html)
    for item in result:
        print(item)


if __name__ == "__main__":

    conn = pymysql.connect(host='localhost', user='root', passwd='', db='my_db')
    cursor = conn.cursor()
    # pool = Pool()
    # pool.map(main, [i * 10 for i in range(10)])
    for i in range(10):
        main(i)

