#!/usr/bin/env
# -*- coding: UTF-8 -*- 

import os
import pandas as pd
import numpy as np
from sklearn.svm import SVC  
from datetime import datetime, timedelta

class OriginData:
    'OriginData 类，可进行数据存储'

    def __init__(self, dirpath='data\\5min\\'):
        """
        类构造函数
            :param self: 类变量本身 
            :param dirpath='data\\5min\\':  数据存放目录的路径
        """   
        self.dirpath = dirpath

    def loadFromDataFrame(self, df):
        if type(df) != pd.DataFrame:
            raise Exception("df is not DataFrame!")
        self.data = df

    def loadFromCSV(self, filename):
        """
        读取指定CSV文件中的数据
            :param self: 类变量本身
            :param filename: csv数据文件路径，包含后缀名
        """
        if os.path.exists(self.dirpath + filename) == False:
            raise Exception("Not exist this file!")
        self.data = pd.read_csv(self.dirpath + filename)

    def getDataFrame(self):
        """
        得到data属性，可能为None
            :param self: 类变量本身
            :returns: 本身储存的DataFream
        """
        if hasattr(self, 'data') == False:
            raise Exception("Please set data first!")
        return self.data

class DataFilter:
    '数据过滤，选择X，然后产生X'

    def __init__(self):
        pass

    def __getDataFrame(self, df):
        """
        辅助函数，得到传入参数中包含的DataFrame。
            :param self: 类变量本身
            :param df: DataFrame或者含有getDataFrame函数的类
        """   
        # 如果df为originData，取出其中数据
        if hasattr(df, 'getDataFrame'):
            return df.getDataFrame()
        elif type(df) == pd.DataFrame:
            return df 
        else:
            raise Exception("The input param is not DataFrame!")

    def __findTimeInterval(self, string):
        """
        辅助函数，通过给定时间判断日期时间间隔，从而进行数据添加。
            :param self: 类变量本身
            :param string: 给定日期，以字符串形式
            :returns: 返回二元组，第一个是日期字符串转为日期的标准str模板，第二个是时间间隔
        """   
        # 通过Date序列中的长度判断读取数据的时间间隔
        if len(string) > 10:
            return '%Y-%m-%d %H:%M:%S', timedelta(0, 300)
        else:
            return '%Y-%m-%d', timedelta()

    def addMissingData(self, df):
        """
        补全未知数据，即不按间隔的数据，补全的数据取平均。
            :param self: 类变量本身
            :param df: DataFrame或者含有getDataFrame函数的类
        """  
        newdata = self.__getDataFrame(df)
        timeformat, interval = self.__findTimeInterval(newdata['date'].values[0])
        times = map(lambda x: datetime.strptime(x, timeformat), newdata['date'])
        # 由于插入会影响DataFrame顺序，因此从后往前插入
        for i in range(len(times))[1:]:
            if times[len(times) - i] - times[len(times) - i - 1] != interval:
                newdata = pd.DataFrame([['data'] + range(len(newdata.columns))], columns=newdata.columns)
                # 第一项设置成add date，其他项取平均
                newdata['date'] = 'add date'
                for i in newdata.columns:
                    if i == 'data':
                        newdata[i] = 'add data'
                    else:
                        newdata[i] = newdata.loc[len(times) - i - 1:len(times) - i - 1, i] + newdata.loc[len(times) - i:len(times) - i, i] / 2
                newdata = newdata[:len(times) - i].append(newdata, ignore_index=True).append(newdata[len(times) - i:], ignore_index=True)
        return newdata

    def filterDataByNames(self, df, names):
        """
        新建新的DataFrame，通过给定names列表过滤数据，在names内的列会被删除。
            :param self: 类变量本身
            :param df: DataFrame或者含有getDataFrame函数的类
            :param names: 可以转换为set的数据类型
            :returns: 返回新的数据
        """   
        newdata = self.__getDataFrame(df)
        # 删除公共集合
        for columnsindex in set(newdata.columns) & set(names):
            del newdata[columnsindex]
        return newdata

    def addColumnByContain(self, df, contain, name='Y'):
        """
        新加入列，其中contain必须是一个集合。
            :param self: 类变量本身
            :param df: DataFrame或者含有getDataFrame函数的类
            :param contain: 给定的集合
            :returns: 返回新的数据
        """
        newdata = self.__getDataFrame(df)
        # 没有sizeof属性，认定不为集合
        if hasattr(contain, '__sizeof__') == False:
            raise Exception("Please input contains!")
        self.name = contain
            

class ModelEngineer:
    '机器学习，数据输出等操作'
    X = None
    y = None
    model = None

    def setX(self, data):
        """
        设置测试集合X值。
            :param self: 类变量本身 
            :param data=None: 给定数据，若为None使用csv数据
        """   
        if type(df) != pd.DataFrame:
            raise Exception("df is not DataFrame!")      
        self.X = self.data

    def setModelType(self, model='mvc'):
        """
        设置模型，可选MVC。
            :param self: 
            :param model: 
        """
        if type(model) != str:
            raise Exception("model is not a string!")
        self.model = model

if __name__ == '__main__':
    ml = OriginData()
    ml.loadFromCSV('000001.csv')
    print ml.data
    ml.setX()
    print ml.X
    ml.setYByLambda('open', lambda x: x > 0)
    ml.y
    a = {}
    print hasattr(a, '__sizeof__')
    print dir(np.array)
    type(ml.X) == pd.DataFrame
