#!/usr/bin/env
# -*- coding: UTF-8 -*- 
__author__ = 'hza'
__date__ = '2018-1-26 15:27'

import numpy as np
import pandas as pd
from sklearn import preprocessing

class NormalizationGallery:
    '数据归一化库类，归一化对DataFrame所有数据'
    '此类为静态类'

    @staticmethod
    def scale(df):
        """
        将数据标准化
            :param df: 传入DataFrame
            :returns: 标准化后的数据
        """
        if not isinstance(df, pd.DataFrame):
            raise Exception("df is not DataFrame!")
        return preprocessing.scale(df)
    
    @staticmethod
    def minMaxScale(df):
        """
        将数据最大最小化标准化
            :param df: 传入DataFrame
            :returns: 标准化后的数据
        """   
        if not isinstance(df, pd.DataFrame):
            raise Exception("df is not DataFrame!")
        return preprocessing.minmax_scale(df)
    
    @staticmethod
    def normalize(df):
        """
        将数据正态分布化
            :param df: 传入DataFrame
            :returns: 标准化后的数据
        """
        if not isinstance(df, pd.DataFrame):
            raise Exception("df is not DataFrame!")
        return preprocessing.normalize(df)
        
    @staticmethod
    def binarize(df):
        """
        将数据二值化
            :param df: 传入DataFrame
            :returns: 标准化后的数据
        """   
        if not isinstance(df, pd.DataFrame):
            raise Exception("df is not DataFrame!")
        return preprocessing.binarize(df)



if __name__ == '__main__':
    df = pd.read_csv('../data/1day/000001.csv')
    del df['date']
    #print df

    # 测试NormalizationGallery类
    NormalizationGallery.scale(df)
    NormalizationGallery.minMaxScale(df)
    NormalizationGallery.normalize(df)
    NormalizationGallery.binarize(df)
