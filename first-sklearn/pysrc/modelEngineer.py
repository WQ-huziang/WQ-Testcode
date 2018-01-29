#!/usr/bin/env
# -*- coding: UTF-8 -*- 

import os
import pandas as pd
import numpy as np
from numpy import matrix
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier 

class ModelEngineer:
    '机器学习，数据输出等操作'

    def __init__(self, methodname='linear regression', trainingpart=0.9, ):
        """
        类初始化函数。
            :param self: 类变量本身
            :param method='linear regression': model类别，可以为'linear regression', 'svc', 'neural netword'
            :param trainingPart=0.9: 训练集占整体的比例，默认为0.9
        """
        if trainingpart <= 0 or trainingpart >=1:
            raise Exception("Training Part is belong to (0, 1)")
        # 设置model
        if methodname == 'linear regression':
            self.model = LinearRegression()
        elif methodname == 'svc':
            self.model = SVC()
            print 'Warning: your\'s y data\'s type need to be int!'
        elif methodname == 'neural netword':
            self.model = MLPClassifier()
            print 'Warning: your\'s y data\'s type need to be int!'
        else:
            methodname = 'linear regression'
            self.model = LinearRegression()
        # 设置其他属性
        self.trainingpart = trainingpart
        self.methodname = methodname
        self.X = None
        self.y = None
        self.train_X = None
        self.test_X = None
        self.train_y = None
        self.test_y = None

    def setX(self, X):
        """
        设置X集合
            :param self: 类变量本身
            :param newdata: 传入的DataFrame
        """
        self.X = X
    
    def addX(self, X):
        """
        添加X集合，如果X未设置，则设置X集合
            :param self: 类变量本身
            :param newdata: 传入的DataFrame
        """   
        if self.X == None:
            self.setX(X)
        self.X += X

    def setY(self, y):
        """
        设置Y集合       
            :param self: 类变量本身
            :param se: 传入的序列
        """
        self.y = y

    def setSMVType(self):
        """
        设置smv模型。
            :param self: 类变量本身
        """
        self.method = 'svm'
        self.model = SVC()

    def setLinearRegression(self):
        """
        设置线性回归模型。
            :param self: 类变量本身
        """
        self.method = 'linear regression'
        self.model = LinearRegression()

    def setNeuralNetword(self):
        """
        设置神经网络模型。
            :param self: 类变量本身
        """
        self.method = 'neural netword'
        self.model = MLPClassifier()

    def train(self):
        """
        进行测试
            :param self: 类变量本身
            :returns: 返回train_x和train_y
        """   
        # 生成此次的训练集和测试集
        self.train_X, self.test_X, self.train_y, self.test_y = train_test_split(self.X, self.y, test_size=(1 - self.trainingpart))
        # 模拟此次训练集合
        self.model.fit(self.train_X, self.train_y)
        # print "Training X'size:", self.train_X.shape
        # print "Training Y'size:", self.train_y.shape
        # print "Training is Over!"
        return self.train_X, self.train_y

    def vertifyTestData(self):
        """
        验证Test数据并返回结果
            :param self: 类变量本身
            :returns: 返回真正的y和预测的y，真正的y在前面
        """  
        predict_y = self.model.predict(self.test_X)
        return self.test_y, predict_y

    def crossVertifyTestData(self):
        """
        交叉验证Test数据并返回结果
            :param self: 类变量本身
            :returns: 返回真正的y和预测的y，真正的y在前面
        """   
        # 进行交叉验证
        predict_y = cross_val_predict(self.model, self.test_X, cv=10)
        return self.test_y, predict_y

    def predict(self, given_X):
        """
        进行预测
            :param self: 类变量本身
            :param given_X: 给定X数据
            :returns: 预测值y
        """   
        return self.model.predict(given_X)

    def getModelMethodName(self):
        """
        得到Model方法值
            :param self: 类变量本身
        """   
        return self.methodname
        

if __name__ == '__main__':
    # 进行数据读取
    data = FastResearchData()
    #print data.getAllFilePath()
    for i in range(400, 500):
        data.addDataFromCSV('000' + str(i) + '.csv')
    #print data.getDataFrameByStockname('000400')
    data.addDataFromKeyValue('mystock', data.concatAllStockData())
    testdata = data.getDataFrameByStockname('mystock')

    # 数据更新
    del testdata['stockname']
    del testdata['open']
    del testdata['date']
    testdata['macd'] = IndicatorGallery.getMACD(testdata.close)
    testdata['ahead_macd'] = IndicatorGallery.getAheadData(testdata.macd, interval=5)
    #testdata['macd'] = RefleshData.predictNanByColumn(testdata, 'macd')
    testdata = RefleshData.deleteRowWithNan(testdata)

    # 测试ModelEngineer类
    me = ModelEngineer()
    me.setX(testdata.iloc[:,:-1])
    me.setY(testdata.iloc[:,-1])
    me.setLinearRegression()
    # 进行模拟
    me.train()
    me.test()
    #me.crossTest()