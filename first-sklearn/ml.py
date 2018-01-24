#!/usr/bin/env
# -*- coding: UTF-8 -*- 

import os
import pandas as pd
import numpy as np

class OriginData:
    'OriginData 类，可进行数据存储'
    dirpath = ''
    data = None

    def __init__(self, dirpath='data\\5min\\'):
        """
        类构造函数
            :param self: 类变量本身 
            :param dirpath='data\\5min\\':  数据存放目录的路径
        """   
        self.dirpath = dirpath

    def loadFromDataFrame(self, df):
        if type(df) != pd.DataFrame:
            raise MyError("df is not DataFrame!")
        self.data

    def loadFromCSV(self, filename):
        """
        读取指定CSV文件中的数据
            :param self: 类变量本身
            :param filename: csv数据文件路径，包含后缀名
        """
        if os.path.exists(self.dirpath + filename) == False:
            raise MyError("Not exist this file!")
        self.data = pd.read_csv(self.dirpath + filename)

class ModelEngineer:
    '机器学习，数据输出等操作'
    X = None
    y = None
    type = None

    def setX(self, data):
        """
        设置测试集合X值。
            :param self: 类变量本身 
            :param data=None: 给定数据，若为None使用csv数据
        """   
        if type(df) != pd.DataFrame:
            raise MyError("df is not DataFrame!")      
        self.X = self.data

    def setyByLambda(self, columns, func):
        """
        设置测试集合y值，对lambda列的所有系数进行func操作得到新的结果。
            :param self: 类变量本身 
            :param columns: 给定列的值，对每该列进行数据处理
            :param func: 给定函数，函数形式为::Float -> Bool/Float，可用lambda表达式
        """
        if type(self.X) == None:
            raise MyError("Please setX first!")
        self.y = map(func, ml.X[columns])

    def setyByContain(self, contain):
        """
        设置测试集合y值，将contain直接赋值给self.y，其中contain必须是一个集合。
            :param self: 类变量本身
            :param contain: 给定的集合
        """
        if type(self.X) == None:
            raise MyError("Please setX first!")
        # 没有sizeof属性，认定不为集合
        if hasattr(contain, '__sizeof__') == false:
            raise MyError("Please input contains!")
        self.y = contain



if __name__ = '__main__':
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
