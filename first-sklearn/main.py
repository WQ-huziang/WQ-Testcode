#coding=utf-8
# main文档

import argparse 
from mymodel import *

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