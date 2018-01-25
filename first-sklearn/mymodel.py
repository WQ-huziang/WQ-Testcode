#!/usr/bin/env
# -*- coding: UTF-8 -*- 

import os
import pandas as pd
import numpy as np
from numpy import matrix
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier 
from sklearn.model_selection import cross_val_predict
from mydata import *

class ModelEngineer:
    '机器学习，数据输出等操作'
    mydata = DataFilter()

    def __init__(self, method='linear regression', trainingPart=0.9, ):
        """
        类初始化函数。
            :param self: 类变量本身
            :param method='linear regression': model类别，可以为'linear regression', 'svc', 'neural netword'
            :param trainingPart=0.9: 训练集占整体的比例，默认为0.9
        """
        if trainingPart <= 0 or trainingPart >=1:
            raise Exception("Training Part is belong to (0, 1)")
        self.method = method
        if method == 'linear regression':
            self.model = LinearRegression()
        elif method == 'svc':
            self.model = SVC()
            print 'Warning: your\'s y data\'s type need to be int!'
        elif method == 'neural netword':
            self.method = MLPClassifier()
            print 'Warning: your\'s y data\'s type need to be int!'
        else:
            method = 'linear regression'
            self.model = LinearRegression()
        self.trainingPart = trainingPart

    def setX(self, newdata):   
        """
        设置X集合       
            :param self: 类变量本身
            :param newdata: 传入的DataFrame
        """   
        self.mydata.loadFromDataFrame(newdata)
    
    def addX(self, newdata):
        """
        添加X集合       
            :param self: 类变量本身
            :param newdata: 传入的DataFrame
        """   
        self.mydata.addFromDataFrame(newdata)

    def setY(self, se):
        """
        设置Y集合       
            :param self: 类变量本身
            :param se: 传入的序列
        """   
        self.mydata.addColumnByContain(se, 'Y')

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
        """   
        newdata = self.mydata.getDataFrame()
        # 生成此次的训练集和测试集
        self.train_X, self.test_X, self.train_y, self.test_y = train_test_split(newdata.iloc[:,:-1], newdata.iloc[:,-1:], test_size=self.trainingPart)
        # 模拟此次训练集合
        self.model.fit(self.train_X, self.train_y)
        print "Training is Over!"
        return self.train_X, self.train_y        

    def evaluateOutSample(self):
        """
        显示输出并绘图
            :param self: 类变量本身
        """  
        predict_y = self.model.predict(self.test_X)
        self.drawTable(self.test_X, predict_y, self.test_y)

    def crossTest(self):
        """
        显示交叉验证结果并绘图
            :param self: 类变量本身
        """   
        # 进行交叉验证
        predict_y = cross_val_predict(self.model, self.test_X, self.test_y, cv=8)
        self.drawTable(self.test_X, predict_y, self.test_y)

    def drawTable(self, X, predict, real):
        """
        画图。
            :param self: 类变量本身
            :param X: X序列
            :param predict: 预测值
            :param real: 实际值
        """   
        X = X.reset_index(drop=True)
        real = real.reset_index(drop=True)
        weight = 1
#         print metrics.classification_report(real, predict)
#         print 'confluse matrix:'
#         print metrics.confusion_matrix(real, predict)
        plt.plot(X.index, real, color='navy', lw=weight, label=self.method + ' model')
        plt.plot(X.index, predict, color='red', lw=weight, label='Real Answer')
        plt.xlabel('X')  
        plt.ylabel('Y')
        plt.legend()  
        plt.show()


    def getData(self):
        """
        得到Data
            :param self: 类变量本身
        """   
        return self.mydata

    def getModelMethodType(self):
        """
        得到Model方法值
            :param self: 类变量本身
        """   
        return self.method
        

if __name__ == '__main__':
    # 测试ModelEngineer类
    me = ModelEngineer()
    me.setLinearRegression()
    mydata = me.getData()
    mydata.loadFromCSV('000001.csv')
    #print mydata.getDataFrame()
    #print mydata
    
    # 修改数据
    mydata.filterDataByNames(['date', 'p_change', 'turnover', 'open', 'high', 'low'])
    mydata.setMACD()
    mydata.setAvgPrc(columnsName='close')
    mydata.shiftColumn(numbers=5)
    
    #dn = DataNormal()
    #normaldata = dn.setNormalizer(mydata.getDataFrame())
    
    # 进行模拟
    me.setLinearRegression()
    #print mydata.getDataFrame()
    me.train()
    me.evaluateOutSample()
    me.crossTest()