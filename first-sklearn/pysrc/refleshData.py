#!/usr/bin/env
# -*- coding: UTF-8 -*- 
__author__ = 'hza'
__date__ = '2018-1-27 14:29'

import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import GradientBoostingRegressor

class RefleshData:
    '数据清洗类，'

    @staticmethod
    def deleteRowWithNan(df):
        return df.dropna().reset_index(drop=True)
    
    @staticmethod
    def setNanByColumn(df, values, columnname):
        return df[columnname].fillna(values, inplace=True)

    @staticmethod
    def predictNanByColumn(df, columnname):
        othercolumns = set(df.columns) - set(columnname)
        notnulldf = df[pd.notnull(df[columnname])]  
        isnulldf = df[pd.isnull(df[columnname])]  
        model = GradientBoostingRegressor()  
        model.fit(notnulldf[othercolumns], notnulldf[columnname])  
        df[columnname][pd.isnull(df[columnname])] = model.predict(isnulldf[othercolumns]) 