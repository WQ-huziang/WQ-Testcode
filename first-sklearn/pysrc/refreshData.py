#!/usr/bin/env
# -*- coding: UTF-8 -*- 
__author__ = 'hza'
__date__ = '2018-1-27 14:29'

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import GradientBoostingRegressor

class RefreshData:
    '数据清洗类，用于处理nan的数据'

    @staticmethod
    def deleteRowWithNan(df):
        """
        删除含有Nan数据的行
            :param df: 传入的DataFrame
            :returns: 返回删除后的DataFrame
        """
        return df.dropna().reset_index(drop=True)
    
    @staticmethod
    def setNanByColumn(df, values, columnname):
        """
        将给定列的nan值修改为给定值
            :param df: 传入的DataFrame
            :param values: 修改的指定值
            :param columnname: 列名
            :returns: 返回修改后的指定列
        """
        return df[columnname].fillna(values)

    @staticmethod
    def predictNanByColumn(df, columnname):
        """
        通过线性回归算法，预测指定列的nan值
            :param df: 传入的DataFrame
            :param columnname: 列名
            :returns: 返回填充后的指定列
        """   
        othercolumns = list(set(df.columns) - set([columnname]))
        notnulldf = df[pd.notnull(df[columnname])]  
        isnulldf = df[pd.isnull(df[columnname])]
        # 创建模型
        model = GradientBoostingRegressor()  
        model.fit(notnulldf[othercolumns], notnulldf[columnname])
        # 预测结果
        notnullse = notnulldf[columnname]
        isnullse = model.predict(isnulldf[othercolumns])
        return notnullse.append(pd.Series(isnullse, index=isnulldf.index)).sort_index()

if __name__ == '__main__':
    df = pd.read_csv('../data/5min/000001.csv')
    del df['date']
    df.open[range(10, 20)] = np.nan
    RefreshData.deleteRowWithNan(df)
    RefreshData.setNanByColumn(df, df.open.mean(), 'open')
    RefreshData.predictNanByColumn(df, 'open')