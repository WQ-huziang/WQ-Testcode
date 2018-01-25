#!/usr/bin/env
#coding=utf-8

import os
import pandas as pd
import numpy as np
from sklearn.svm import SVC  
from datetime import datetime, timedelta
from sklearn import preprocessing

class OriginData:
    'OriginData 类，可进行数据存储'

    def __init__(self, dirpath='data\\5min\\', data=None):
        """
        类构造函数
            :param self: 类变量本身 
            :param dirpath='data\\5min\\':  数据存放目录的路径
        """   
        self.dirpath = dirpath
        if type(data) == pd.DataFrame:
            self.data = data

    def loadFromDataFrame(self, df):
        """
        载入数据
            :param self: 类变量本身
            :param df: 传入的DataFrame
        """
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

    def addFromDataFrame(self, df):
        """
        添加DataFrame，如果类内data为空，等同于loadFromDataFrame
            :param self: 类变量本身
            :param df: 与类内匹配的DataFrame
        """   
        if type(df) != pd.DataFrame:
            raise Exception("df is not DataFrame!")
        elif hasattr(self, 'data') == False:
            self.data = df
        else:
            self.data = self.data.append(df, ignore_index=True)


    def getDataFrame(self):
        """
        得到data属性，可能为None
            :param self: 类变量本身
            :returns: 本身储存的DataFream
        """
        if hasattr(self, 'data') == False:
            raise Exception("Please set data first!")
        return self.data

    def setDirPath(self, dirpath):
        """
        设置文件夹路径
            :param self: 类变量本身
            :param dirpath: 类内部的dirpath
        """   
        self.dirpath = dirpath

class DataFilter(OriginData):
    '数据过滤类，可以选择X，产生X，生成Y'

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

    def __calEMA(self, N, a, b):
        """
        辅助函数，计算EMA的值。
            :param self: 类变量本身 
            :param N: 第N项
            :param a: close_price_today
            :param b: ema_yesterday
        """   
        return 2 / float(N + 1) * (a - b) + b

    def addMissingData(self):
        """
        补全未知数据，即不按间隔的数据，补全的数据取平均。
            :param self: 类变量本身
        """  
        newdata = self.getDataFrame()
        timeformat, interval = self.__findTimeInterval(newdata['date'].values[0])
        times = map(lambda x: datetime.strptime(x, timeformat), newdata['date'])
        # 由于插入会影响DataFrame顺序，因此从后往前插入
        for i in range(len(times))[1:]:
            if times[len(times) - i] - times[len(times) - i - 1] != interval:
                newdata = pd.DataFrame([['data'] + range(len(newdata.columns) - 1)], columns=newdata.columns)
                # 第一项设置成add date，其他项取平均
                newdata['date'] = 'add date'
                for j in newdata.columns:
                    if j == 'data':
                        newdata[j] = 'add data'
                    else:
                        newdata[j] = newdata.loc[len(times) - i - 1:len(times) - i - 1, j] + newdata.loc[len(times) - i:len(times) - i, j] / 2
                newdata = newdata[:len(times) - i].append(newdata, ignore_index=True).append(newdata[len(times) - i:], ignore_index=True)

    def filterDataByNames(self, names):
        """
        新建新的DataFrame，通过给定names列表过滤数据，在names内的列会被删除。
            :param self: 类变量本身
            :param names: 可以转换为set的数据类型
        """   
        newdata = self.getDataFrame()
        # 删除公共集合
        for columnsindex in set(newdata.columns) & set(names):
            del newdata[columnsindex]

    def addColumnByContain(self, contain, name):
        """
        新加入列，其中contain必须是一个集合。
            :param self: 类变量本身
            :param contain: 给定的集合
            :param name: 新的列名
        """
        newdata = self.getDataFrame()
        # 没有sizeof属性，认定不为集合
        if hasattr(contain, '__sizeof__') == False:
            raise Exception("Please input contains!")
        newdata[name] = contain

    def shiftColumn(self, name=None, numbers=1):
        """
        将某行向上移动numbers，并删除最后的numbers行
            :param self: 类的变量名
            :param name=None: 移动行的名字，若为None，移动最后一行
            :param numbers=1: 移动位数
        """   
        newdata = self.getDataFrame()
        if name == None:
            newdata.iloc[:,-1].shift(-numbers)
        else:
            newdata[name].shift(-numbers)
        newdata = newdata[:-numbers]
        

    def setAvgPrc(self, columnsName="price_change", interval=10):
        """
        计算平均值，其中平均值新建一列，该列的名字为原列+'_avg'。
            :param self: 类变量本身
            :param columnsName="price_change": 列名
            :param interval=10: 间隔数，当前值取前interval个求平均
        """
        newdata = self.getDataFrame()
        # 由于没找到深复制的方法，因此新建了一列
        self.addColumnByContain(newdata[columnsName], columnsName + '_avg')
        se, se_avg = newdata[columnsName], newdata[columnsName + '_avg']
        # 前interval个取平均，如果之前的数量少于interval，则之前全部取平均
        [se_avg.set_value(i, np.mean(se[max(0, i - interval):i + 1])) for i in range(len(se_avg))]

    def setMACD(self, columnsName='close', short=12, llong=26, di=9):
        """
        计算MACD的值，其中MACD新建一列，该列名字为原列+'_macd'。
        MACD[i + 1] = 2 * a * (emashort[i + 1] - emalong[i + 1] - MACD[i]) - MACD[i]
            :param self: 类变量本身
            :param columnsName='close': 列名，默认为close，即关盘价格
            :param short=12: short ema的a值，一般为12
            :param llong=26: long ema的a值，一般为26
            :param di=9: diff的a值，一般为9
        """   
        newdata = self.getDataFrame()
        # 由于没找到深复制的方法，因此新建了一列
        self.addColumnByContain(newdata[columnsName], columnsName + '_macd')
        se, se_macd = newdata[columnsName], newdata[columnsName + '_macd']
        # 初始化第一个值
        emashort, emalong = newdata[columnsName][0], newdata[columnsName][0]
        se_macd[0] = emashort - emalong 
        # 递归计算MACD
        for i in range(len(se_macd))[1:]:
            emashort = self.__calEMA(short, newdata[columnsName][i], emashort)
            emalong = self.__calEMA(llong, newdata[columnsName][i], emalong)
            se_macd[i] = self.__calEMA(di, 2 * (emashort - emalong), se_macd[i - 1])
        

class DataNormal:
    '数据归一化类，归一化对X和Y同时进行归一化，此时数据包含X和Y'

    def setScale(self, df):
        """
        设置数据标准化器
            :param self: 类变量本身
            :param df: 传入DataFrame
        """   
        if type(df) != pd.DataFrame:
            raise Exception("df is not DataFrame!")
        # 定义归一化器
        self.type = 'scale'
        self.process = preprocessing.StandardScaler().fit(df)
    
    def setMinMaxScale(self, df):
        """
        设置数据最大最小化标准化器
            :param self: 类变量本身
            :param df: 传入DataFrame
        """   
        if type(df) != pd.DataFrame:
            raise Exception("df is not DataFrame!")
        # 定义归一化器
        self.type = 'minmaxscale'
        self.process = preprocessing.MinMaxScaler().fit(df)
    
        
    def setNormalizer(self, df):
        """
        设置数据最大最小化标准化器
            :param self: 类变量本身
            :param df: 传入DataFrame
        """   
        if type(df) != pd.DataFrame:
            raise Exception("df is not DataFrame!")
        # 定义归一化器
        self.type = 'normal'
        self.process = preprocessing.Normalizer().fit(df)
        
    def setBinarizer(self, df):
        """
        设置数据最大最小化标准化器
            :param self: 类变量本身
            :param df: 传入DataFrame
        """   
        if type(df) != pd.DataFrame:
            raise Exception("df is not DataFrame!")
        # 定义归一化器
        self.type = 'binarizer'
        self.process = preprocessing.Binarizer().fit(df)

    def getScaleType(self):
        """
        得到scale的类型。
            :param self: 类变量本身
            :returns: 返回一个字符串，如果未设置，抛出Excpetion错误 
        """  
        if hasattr(self, 'type') == False:
            raise Exception("Please set scale first!")
        else:
            return self.type
    
    def processData(self, df):
        """
        归一化指定DataFrame，如果scale未设置，抛出Exception错误
            :param self: 类变量本身
            :param df: 传入DataFrame
            :returns: 返回归一化后的array
        """   
        if type(df) != pd.DataFrame:
            raise Exception("df is not DataFrame!")
        # 检验scale是否存在
        self.getScaleType()
        return self.process.transform(df)

if __name__ == '__main__':
    # 测试OriginData类
    data = OriginData()
    #data.loadFromCSV('000200.csv')
    #print data.dirpath + '000001.csv'
    #data.loadFromCSV('000001.csv')
    #print data.getDataFrame(), len(data.getDataFrame())
    df = pd.read_csv(data.dirpath + '000001.csv')

    # 测试DataFilter类
    data = DataFilter()
    #print data.dirpath + '000001.csv'
    #data.loadFromCSV('000001.csv')
    #print data.getDataFrame(), len(data.getDataFrame())
    #df = pd.read_csv(data.dirpath + '000002.csv')
    #print df
    #data.addFromDataFrame(df)
    #print len(data.data)
    #data.addMissingData()
    #print len(data.data)
    #data.filterDataByNames(['date', 'ma10', 'ma20'])
    
    #data.addColumnByContain(range(len(data.getDataFrame())), 'test')
    #print data.data.columns
    #test = pd.read_csv('data\\5min\\000011.csv')
    #test['test'] = range(len(test))
    #print test.columns

    #data.setAvgPrc('open', 10)
    #print data.getDataFrame()['open_avg']
    
    #data.setMACD()
    # print data.getDataFrame()['close_macd']

    df.iloc[:,-1].shift(1)
    df = df[1:]
    print df
    
    # 测试DataNormal类
    dm = DataNormal()
    dm.setNormalizer(df.iloc[:,1:])
    t = dm.processData(df.iloc[:,1:])
    print t
    