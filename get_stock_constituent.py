#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2019-02-25 10:02 
# @Author : hexiaoxiong
# @File : get_stock_constituent.py 


from fake_useragent import UserAgent
import requests
import re
import json


def get_url(index, page):
	return 'http://stock.finance.sina.com.cn/usstock/api/jsonp.php//US_CategoryService.getChengfen?page={}&num=30&type={}'.format(page, index)

def tojson(s):
	'''
	当爬取的类似json格式字符串的key没有加双引号时，此函数可以添加上双引号
	'''
	if '\\' in s:
		s = s.replace('\\', '')
	if s[s.index(':') - 1] != '"'"":  # index  rindex都可以
		return re.sub(r'(?<={|,)(\w+?)(?=:)', r'"\1"', s)  # 前瞻：exp1(?=exp2) 查找exp2前面的exp1；后顾：(?<=exp2)exp1 查找exp2后面的exp1；负前瞻：exp1(?!exp2) 查找后面不是exp2的exp1；负后顾：(?<!=exp2)exp1 查找前面不是exp2的exp1    |表示或    r'"\1"'替换为"第一个子表达式内容"
	else:
		return s


def get_stocks_text(url):
	headers = {'User-agent': UserAgent().random}
	stocks = requests.get(url, headers = headers)
	stocks_text = stocks.text
	if stocks_text[-1] == ';':
		stocks_text = stocks_text[2: -3]
	else:
		stocks_text = stocks_text[2: -2]
	return stocks_text


def get_stockindex(indexname):
	if indexname == '标普500':
		index = 2
	elif indexname == '道琼斯':
		index = 3
	elif indexname == '纳斯达克':
		index = 1
	else:
		print('指数名错误')
	page = 1
	stockslist = list()
	while True:
		url = get_url(index, page)
		stocks_text = get_stocks_text(url)
		stocks_list = json.loads(tojson(stocks_text))['data']
		if len(stocks_list) > 0:
			stockslist += stocks_list
			page += 1
		else:
			break
	return stockslist
	

if __name__ == '__main__':
	stocks_list = get_stockindex('标普500')
	stocks = list()
	for d in stocks_list:
		stocks.append(d['symbol'])
	print(stocks)

