#!/usr/bin/env
# -*- coding: UTF-8 -*- 

import os
import pandas as pd
import numpy as np

class ML:
    'machine learning 类，可进行数据存储，机器学习，数据输出等操作'
    dirpath = ''
    csvdata = None
    traindata = None
    testdata = None

    def __init__(self, dirpath='data\\1day\\'):
        """
        类构造函数
            :param self: 类变量 
            :param dirpath='data\\1day\\':  数据存放目录的路径
        """   
        self.dirpath = dirpath

    def readCSVData(self, filename):
        '''
        读取指定CSV文件中的数据
        :param filename: 存放数据的文件名，包含后缀
        '''
        if !os.path.exists(self.dirpath + filename):
            raise NotFileError("No such file!")
        csvdata = pd.read_csv(self.dirpath + filename)