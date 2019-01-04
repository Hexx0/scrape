#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 20:02:53 2018

@author: hexiaoxiong
"""

from collections import Counter
import tushare as ts
import pandas as pd
import numpy as np
# 导入相关模块

ts.set_token('c80037f3bab1a7c31425e34de0805a52edd8435f52fe6c9cec9ad200')
pro=ts.pro_api()# 创建tushare接口

df=pd.read_excel('研报.xlsx')# 读取爬取的研报数据
a=Counter(df['证券代码'])# 统计证券代码出现的频率
data=pd.DataFrame()# 创建一个空的DataFrame数据表
for i in range(50):# 获取股票数据，并存入data数据表中
    data[a.most_common(50)[i][0]]=pro.query('daily',ts_code=a.most_common(50)[i][0],start_date='20180509',end_date='20181112',fields='close')['close']
    
data['trade_date']=pro.query('daily',ts_code='600426.SH',start_date='20180509',end_date='20181112')['trade_date']
data.set_index('trade_date',inplace=True)
data.sort_index(ascending=True,inplace=True)   

for i in data.columns:# 剔除含有空值的股票
    if True in data[i].isnull().values:
        print(i)
        data.drop(i,axis=1,inplace=True)

#收益率回归
data1=np.log(data)
data1=data1.diff(1)
data1.drop(index='20180509',inplace=True)

import statsmodels.formula.api as smf
df4=pd.DataFrame()
df5=pd.DataFrame()

for i in data1.columns:
    df4['r']=data1[i]
    df4['rlag1']=df4['r'].shift(-1)
    df4['e']=df3[i]
    df4['elag1']=df4['e'].shift(-1)
    results=smf.ols('r~e',data=df4).fit()
    
    df5[i]=[results.params[1],results.pvalues[1]]
df5.index=['params','pvalue']
df5=df5.T



#成交量回归
dat=pd.DataFrame()
for i in range(50):
    dat[a.most_common(50)[i][0]]=pro.query('daily',ts_code=a.most_common(50)[i][0],start_date='20180509',end_date='20181112',fields='vol')['vol']
    
dat['trade_date']=pro.query('daily',ts_code='600426.SH',start_date='20180509',end_date='20181112')['trade_date']
dat.set_index('trade_date',inplace=True)
dat.sort_index(ascending=True,inplace=True)


for i in dat.columns:
    if True in dat[i].isnull().values:
        print(i)
        dat.drop(i,axis=1,inplace=True)
dat.drop(index='20180509',inplace=True)
        
import statsmodels.formula.api as smf

df4=pd.DataFrame()
df5=pd.DataFrame()

for i in dat.columns:
    df4['r']=dat[i]
    df4['rlag1']=df4['r'].shift(-1)
    df4['e']=df3[i]
    df4['elag1']=df4['e'].shift(-1)
    results=smf.ols('r~e',data=df4).fit()
    
    df5[i]=[results.params[1],results.pvalues[1]]

df5.index=['params','pvalue']
df5=df5.T



#换手率回归
hsl=pd.DataFrame()
for i in range(50):
    hsl[a.most_common(50)[i][0]]=pro.query('daily_basic',ts_code=a.most_common(50)[i][0],start_date='20180509',end_date='20181112',fields='turnover_rate_f')['turnover_rate_f']
    
hsl['trade_date']=pro.query('daily',ts_code='600426.SH',start_date='20180509',end_date='20181112')['trade_date']
hsl.set_index('trade_date',inplace=True)
hsl.sort_index(ascending=True,inplace=True)

for i in hsl.columns:
    if True in hsl[i].isnull().values:
        print(i)
        hsl.drop(i,axis=1,inplace=True)
hsl.drop(index='20180509',inplace=True)

import statsmodels.formula.api as smf
df4=pd.DataFrame()
df5=pd.DataFrame()

for i in hsl.columns:
    df4['r']=hsl[i]
    df4['rlag1']=df4['r'].shift(-1)
    df4['e']=df3[i]
    df4['elag1']=df4['e'].shift(-1)
    results=smf.ols('r~e',data=df4).fit()
    
    df5[i]=[results.params[1],results.pvalues[1]]
df5.index=['params','pvalue']
df5=df5.T

# 截面回归
import statsmodels.formula.api as smf
df5=pd.DataFrame()
date=['20180521','20180706','20180717','20180808']
for i in data1.index:
    df4=pd.DataFrame()
    
    df4['r']=data1.loc[i]
    
    df4['e']=df3.loc[i]
    
    results=smf.ols('r~e',data=df4).fit()
    
    df5[i]=[results.params[1],results.pvalues[1]]
df5.index=['params','pvalue']
df5=df5.T

# 将研报文本数据转为0-1虚拟变量
df1=pd.DataFrame()
df2=pd.DataFrame()
df3=pd.DataFrame()
df2['日期']=data1.index
df.set_index('证券代码',inplace=True)
for i in data.columns:
    df1=df.loc[i,['日期','原文评价']]
    df1.drop_duplicates('日期',inplace=True)
    df3[i]=df2.set_index('日期').join(df1.set_index('日期'))['原文评价']

df3.fillna(0,inplace=True)   
df3.replace('买入',1,inplace=True)
df3.replace('增持',1,inplace=True)
df3.replace('中性',0,inplace=True)
df3.replace('减持',-1,inplace=True)
df3.replace('卖出',-1,inplace=True)
df3.replace('持有',0,inplace=True)


from linearmodels import PanelOLS
