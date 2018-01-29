#!/usr/bin/env
# -*- coding: UTF-8 -*- 
__author__ = 'hza'
__date__ = '2018-1-28 18:54'

from fastResearchData import FastResearchData
from indicatorGallery import IndicatorGallery
from RefreshData import RefreshData
from normalizationGallery import NormalizationGallery
from modelEngineer import ModelEngineer
from drawPlot import DrawPlot

import os
import random
import argparse
import pandas as pd
import numpy as np
from datetime import datetime

def setArgParse():
    '''
    设置argparse
    '''
    parser = argparse.ArgumentParser(description='The program using given data to predict target data.')
    # 必选参数
    parser.add_argument(
        'beginstockcode',
        help='The begin stock\'s code, must be int type',
        type=int
    )
    parser.add_argument(
        'endstockcode',
        help='The end stock\'s code, must be int type',
        type=int
    )
    parser.add_argument(
        'columnname',
        help='The name of column that you want to predict',
        type=str
    )
    # 可选参数
    parser.add_argument(
        '-d',
        '--dirpath',
        help='Given data folder path, if not set, the path is \'../data/5min/',
        type=str,
        default='../data/5min/'
    )
    parser.add_argument(
        '-r',
        '--reflesh',
        help='Whether reflesh stock data',
        action='store_true'
    )
    parser.add_argument(
        '-s',
        '--smallrelevance',
        help='The smallest relevance, if the relevance between tag in X and y is small than it, it will be deleted',
        type=float,
        default=0.5
    )
    parser.add_argument(
        '-b',
        '--bigrelevance',
        help='The bigest relevance, if the relevance between tag in X and y is big than it, it will be deleted',
        type=float,
        default=1.0
    )
    parser.add_argument(
        '-m',
        '--modelengineer',
        help='The model engineer you want to select',
        type=str,
        default='linear regression',
        choices=['linear regression', 'neural netword', 'svm']
    )
    parser.add_argument(
        '-i',
        '--interval',
        help='The interval you want to predict',
        type=int,
        default=10,
    )
    return parser.parse_args()
    

if __name__ == '__main__':
    # 设置参数
    args = setArgParse()

    # 导入数据
    fastdata = FastResearchData()
    for index in range(args.beginstockcode, args.endstockcode):
        fastdata.addDataFromCSV("%06d" % index + '.csv')
    if len(fastdata.getDatadict()) == 0:
        print 'Don\'t load any data! Please check the dirpath and stockcodes:'
        print '\tdirpath = ' + args.dirpath
        print '\tstockcodes is [' + ("%06d" % args.beginstockcode) + ', ' + ("%06d" % args.endstockcode) + ')'
        exit(1)
    
    print 'Load Stock Data Finish!'
    print 'Load stock\'s num is', len(fastdata.getDatadict().keys()), '\n'

    # 输入预测数据
    predictcolumn = args.columnname
    if predictcolumn not in list(fastdata.getDatadict().values()[0].columns):
        print 'The columns\' name list as follow:'
        print '\t', list(fastdata.getDatadict().values()[0].columns)
        print 'What columns do you want to predict?',
        while True:
            predictcolumn = raw_input()
            if predictcolumn in list(fastdata.getDatadict().values()[0].columns):
                break
            print 'Your input is wrong, Please choice a column:',

    concatdf = fastdata.concatAllStockData()
    # 进行数据清洗，如果预测的数据时间不对，会被赋值成nan
    if args.reflesh:
        calfunc = lambda ls : ls[-1]
        filfunc = lambda df, time, inv, ind : \
            int((datetime.strptime(df.date[ind + inv], "%Y-%m-%d %H:%M:%S") - datetime.strptime(df.date[ind], "%Y-%m-%d %H:%M:%S")).total_seconds()) / 300 == inv
        concatdf[predictcolumn + 'predict'] = IndicatorGallery.getAheadCalWithFilter(
            concatdf[predictcolumn],
            calfunc,
            filfunc,
            [concatdf, 300, args.interval],
            args.interval
        )
        print 'Clean Stock Data Finish!'
        print 'Stock data\'s size is', len(concatdf), '\n'
    # 普通的前移数据
    else:
        concatdf[predictcolumn + 'predict'] = IndicatorGallery.getAheadData(concatdf[predictcolumn], args.interval)
    
    # 去除含有nan的数据
    concatdf = RefreshData.deleteRowWithNan(concatdf)

    print 'Refresh Data Finish!'
    print 'Remain stock data\'s size is', len(concatdf), '\n'

    # 去除相关性太高或太低的列
    del concatdf['date']
    del concatdf['stockname']
    othercolumn = list(set(concatdf.columns) - set([predictcolumn]))
    for column in othercolumn:
        corrvalue = abs(concatdf[predictcolumn].corr(concatdf[column]))
        if corrvalue < args.smallrelevance or corrvalue > args.bigrelevance:
            del concatdf[column]
    
    print 'Set X and Y Finish!'
    print 'X\'s columns is', list(concatdf.columns), '\n'

    # 建立模型
    othercolumn = list(set(concatdf.columns) - set([predictcolumn]))
    me = ModelEngineer(args.modelengineer)
    me.setX(concatdf[othercolumn])
    me.setY(concatdf[predictcolumn])
    me.train()
    
    print 'Build model finish!\n'

    # 随机进行测试
    random.seed()
    randomnum = random.randint(1, 999999)
    while not os.path.exists(args.dirpath + "%06d" % randomnum + '.csv'):
        randomnum = random.randint(1, 999999)
    X = pd.read_csv(args.dirpath + "%06d" % randomnum + '.csv')
    real_y = pd.Series(X[predictcolumn], name='real')
    predict_y = pd.Series(me.predict(X[othercolumn]), name='predict')

    print 'Test Finish!'
    print 'The tested stock is', "%06d" % randomnum

    # 显示预测结果图
    dp = DrawPlot("%06d" % randomnum + ' stock predict plot')
    dp.drawLinePlot(real_y, predict_y)
    dp.drawJointPlot(real_y, predict_y)
    dp.drawDensityCurvePlot(real_y - predict_y)