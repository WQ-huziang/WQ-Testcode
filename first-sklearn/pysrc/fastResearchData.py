#!/usr/bin/env
# -*- coding: UTF-8 -*- 
__author__ = 'hza'
__date__ = '2018-1-27 9:13'

import os
import pandas as pd
import numpy as np
from sklearn.svm import SVC  

class FastResearchData:
    'FastResearchData类，使用dict数据结构，可进行数据存储'

    def __init__(self, dirpath='../data/5min/'):
        """
        类构造函数
            :param self: 类变量本身 
            :param dirpath='../data/5min/':  数据存放目录的路径
        """   
        self.dirpath = dirpath
        self.stockdata = {}

    def addDataFromKeyValue(self, stockname, df):
        """
        载入数据，传入Key值和Value值，Value值为DataFrame
            :param self: 类变量本身
            :param stockname: 股票名称
            :param df: 传入的DataFrame
        """
        if not isinstance(df, pd.DataFrame):
            #print "df is not DataFrame!"
            return
        self.stockdata[str(stockname)] = df.sort_values(by='date').reset_index(drop=True)

    def addDataFromCSV(self, filename):
        """
        读取指定CSV文件中的数据，键值设置为文件名
            :param self: 类变量本身
            :param filename: csv数据文件路径，包含后缀名
        """
        if os.path.exists(self.dirpath + filename) == False:
            #print "Not exist " + filename +" file!"
            return
        self.stockdata[filename[filename.rfind('/') + 1:filename.rfind('.')]] = pd.read_csv(self.dirpath + filename).sort_values(by='date').reset_index(drop=True)


    def delDataByStockname(self, stockname):
        """
        通过stockname删除指定数据
            :param self: 类变量本身
            :param stockname: 股票名称
        """
        del self.stockdata[str(stockname)]

    def concatAllStockData(self):
        """
        将所有的DataFrame连接，然后返回，新的DataFrame增加一行stockname，是每个股票的stockname
            :param self: 类变量本身
            :returns: 所有连接的DataFrame
        """   
        # 新建dataframe，列多一行
        tempstockdata = self.stockdata.items()[0][1]
        allstockdata = pd.DataFrame(columns=['stockname'] + tempstockdata.columns.tolist())
        # 循环加入
        for stockname, dataframe in self.stockdata.items():
            appenddataframe = pd.concat([dataframe, pd.Series(np.full(len(dataframe), int(stockname)), name='stockname')], axis=1)
            allstockdata = allstockdata.append(appenddataframe, ignore_index=True)
        # 重新排序，重新设置下标
        allstockdata = allstockdata.sort_index(ascending=True)
        allstockdata = allstockdata.reset_index(drop=True)
        return allstockdata

    def setDatadict(self, datadict):
        """
        docstring here
            :param self: 类变量本身
            :param datadict: 传入的字典
        """   
        if not isinstance(datadict, dict):
            raise Exception('datadict is not a dict!')
        self.stockdata = datadict

    def getDatadict(self):
        """
        得到结构里储存的字典数据
            :param self: 类变量本身
            :returns: 类储存的股票数据
        """   
        return self.stockdata

    def getDataFrameByStockname(self, stockname):
        """
        通过股票名称得到data属性，可能为None
            :param self: 类变量本身
            :param stockname: 股票名称
            :returns: 本身储存的DataFream
        """
        return self.stockdata[str(stockname)]

    def setDirPath(self, dirpath):
        """
        设置文件夹路径
            :param self: 类变量本身
            :param dirpath: 类内部的dirpath
        """   
        self.dirpath = dirpath

    def getDirPath(self):
        """
        得到类变量dirpath
            :param self: 类变量本身
            :returns: 类内部dirpath
        """
        return self.dirpath

    def getAllFilePath(self, filetype='.csv'):
        """
        得到dirpath路径下的所有.csv文件的相对路径
            :param self: 类变量本身
            :param filetype=',csv': 文件类型种类，带.
            :returns: 所有同类型文件的相对路径
        """
        filepathlist = []
        for _, _, names in os.walk(self.dirpath):
            filepathlist += filter(lambda f : os.path.splitext(f)[1] == filetype, names)
        return filepathlist

if __name__ == '__main__':
    # 测试FastResearchData类
    data = FastResearchData()
    data.getAllFilePath()
    data.addDataFromCSV('000001.csv')
    data.getDataFrameByStockname('000001')
    test = pd.read_csv('../data/5min/000002.csv')
    data.addDataFromKeyValue('000002', test)
    data.getDataFrameByStockname('000002')
    data.concatAllStockData()
    data.delDataByStockname('000001')
    data.getDatadict()
    