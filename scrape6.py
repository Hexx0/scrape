#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 12:04:29 2018

@author: hexiaoxiong
"""

import requests, ast, random, time
import pandas as pd
import fake_useragent as fu
# 导入需要的模块


headers={'User-Agent':fu.UserAgent(verify_ssl=False).random}
# 设置请求头，防止被网站识别为python脚本文件而禁止访问

def get_url(p):
    '''
    此函数用于获取东方财富网个股研报的链接
    '''
    s1='http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20MXaJqeYX={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p='  
    s4='&mkt=0&stat=0&cmd=2&code=&rt=51394'
    s5=str(random.randint(750,950))      
    return s1+str(p)+s4+s5
    

def get_page(url):
    '''
    此函数用于获取链接中关于个股研报的相关数据
    '''
    response=requests.get(url,headers=headers)
    if response.status_code==200:# 如果状态码为200，说明成功访问网页
        a=ast.literal_eval(response.text[13:])# 将爬取的字符串转换为字典格式
    else:
        print('error')
    return a['data']
  
def main(n):
    '''
    此函数将爬取的数据存储为DataFrame数据表
    '''
    e={}# 定义一个空字典
    e['日期']=[]# 给字典加入键和空值
    e['证券代码']=[]
    e['证券名称']=[]
    e['公司代码']=[]
    e['标题']=[]
    e['原文评价']=[]
    e['评级变动']=[]
    e['机构名称']=[]
    e['机构代码']=[]
    e['机构星级']=[]
    e['2018预测市盈率']=[]
    e['2019预测市盈率']=[]
    e['2020预测市盈率']=[]
    e['2017每股收益']=[]
    e['2018预测每股收益']=[]
    e['2019预测每股收益']=[]
    e['2020预测每股收益']=[]
    e['2018预测归属母公司净利润']=[]
    e['2019预测归属母公司净利润']=[]
    e['2020预测归属母公司净利润']=[]
    
    for i in range(1,n):# 将爬取的数据存入字典中
        for item in get_page(get_url(i)):
            
            e['日期'].append(item['datetime'])
            e['证券代码'].append(item['secuFullCode'])
            e['证券名称'].append(item['secuName'])
            e['公司代码'].append(item['companyCode'])
            e['标题'].append(item['title'])
            e['原文评价'].append(item['rate'])
            e['评级变动'].append(item['change'])
            e['机构名称'].append(item['insName'])
            e['机构代码'].append(item['insCode'])
            e['机构星级'].append(item['insStar'])
            e['2018预测市盈率'].append(item['syls'][0])
            e['2019预测市盈率'].append(item['syls'][1])
            e['2020预测市盈率'].append(item['syls'][2])
            e['2017每股收益'].append(item['sy'])
            e['2018预测每股收益'].append(item['sys'][0])
            e['2019预测每股收益'].append(item['sys'][1])
            e['2020预测每股收益'].append(item['sys'][2])
            e['2018预测归属母公司净利润'].append(item['jlrs'][0])
            e['2019预测归属母公司净利润'].append(item['jlrs'][1])
            e['2020预测归属母公司净利润'].append(item['jlrs'][2])
        time.sleep(0.05)# 每一次循环间隔0.05秒，以免访问太快触发网站反爬机制
    return pd.DataFrame(e)# 返回一个DataFrame数据表
    
