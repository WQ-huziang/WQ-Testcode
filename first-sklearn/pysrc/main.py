#!/usr/bin/env
# -*- coding: UTF-8 -*- 
__author__ = 'hza'
__date__ = '2018-1-28 18:54'

from fastResearchData import FastResearchData
from indicatorGallery import IndicatorGallery
from refreshData import RefreshData
from normalizationGallery import NormalizationGallery
from modelEngineer import ModelEngineer
from drawPlot import DrawPlot
from cmdColor import *
from cmdProcessBar import CMDProcessBar

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
    parser.add_argument(
        '-f',
        '--function',
        help='The function you want to select',
        type=str,
        default='',
        choices=['avg', 'min', 'max', 'sum']
    )
    return parser.parse_args()
    

if __name__ == '__main__':
    # CMD颜色
    lintcmdcolor = CMDColor(FOREGROUND_RED)
    datacmdcolor = CMDColor(FOREGROUND_DARKSKYBLUE)

    # 设置参数
    args = setArgParse()

    # STEP1:导入数据
    fastdata = FastResearchData()
    processbar = CMDProcessBar(args.endstockcode - args.beginstockcode)
    for index in range(args.beginstockcode, args.endstockcode):
        processbar.showProcess()
        fastdata.addDataFromCSV("%06d" % index + '.csv')
    processbar.close('Load Data Done!\n')
    if len(fastdata.getDatadict()) == 0:
        print 'Don\'t load any data! Please check the dirpath and stockcodes:'
        print '\tdirpath = ' + args.dirpath
        print '\tstockcodes is [' + ("%06d" % args.beginstockcode) + ', ' + ("%06d" % args.endstockcode) + ')'
        exit(1)
    

    lintcmdcolor.printWithColor('Load Stock Data Finish!\n')
    print 'Load stock\'s num is ',
    datacmdcolor.printWithColor(str(len(fastdata.getDatadict().keys())) + '\n')


    # 如果预测数据不准确，则输入预测数据
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


    # STEP2:数据筛选，求出Y值
    concatdf = fastdata.concatAllStockData()
    # 筛选计算函数
    if args.function == 'avg':
        calfunc = np.average
    elif args.function == 'min':
        calfunc = np.min
    elif args.function == 'max':
        calfunc = np.max
    elif args.function == 'sum':
        calfunc = np.sum
    else:
        calfunc = lambda ls : ls[-1]

    # 进行数据清洗，如果预测的数据时间不对，会被赋值成nan
    if args.reflesh:
        filfunc = lambda df, time, inv, ind : \
            int((datetime.strptime(df.date[ind + inv], "%Y-%m-%d %H:%M:%S") - datetime.strptime(df.date[ind], "%Y-%m-%d %H:%M:%S")).total_seconds()) / 300 == inv
        concatdf[predictcolumn + 'predict'] = IndicatorGallery.getAheadCalWithFilter(
            concatdf[predictcolumn],
            calfunc,
            filfunc,
            [concatdf, 300, args.interval],
            args.interval
        )
        lintcmdcolor.printWithColor('Clean Stock Data Finish!\n')
        print 'Stock data\'s size is ',
        datacmdcolor.printWithColor(str(len(concatdf)) + '\n')
    # 普通的前移数据
    else:
        concatdf[predictcolumn + 'predict'] = IndicatorGallery.getAheadCal(concatdf[predictcolumn], calfunc, args.interval)
    
    # STEP3:数据刷新，去除含有nan的数据
    concatdf = RefreshData.deleteRowWithNan(concatdf)


    lintcmdcolor.printWithColor('Refresh Data Finish!\n')
    print 'Remain stock data\'s size is ',
    datacmdcolor.printWithColor(str(len(concatdf)) + '\n')


    # STEP4:去除相关性太高或太低的列，得到正确X
    del concatdf['date']
    del concatdf['stockname']
    othercolumn = list(set(concatdf.columns) - set([predictcolumn]))
    for column in othercolumn:
        corrvalue = abs(concatdf[predictcolumn].corr(concatdf[column]))
        if corrvalue < args.smallrelevance or corrvalue > args.bigrelevance:
            del concatdf[column]
    

    lintcmdcolor.printWithColor('Set X and Y Finish!\n')
    print 'X\'s columns is ',
    datacmdcolor.printWithColor(str(list(othercolumn)) + '\n')
    print 'Y\'s column is ',
    datacmdcolor.printWithColor(str(predictcolumn) + '\n')


    # STEP5:建立模型
    othercolumn = list(set(concatdf.columns) - set([predictcolumn]))
    me = ModelEngineer(args.modelengineer)
    me.setX(concatdf[othercolumn])
    me.setY(concatdf[predictcolumn])
    me.train()
    

    lintcmdcolor.printWithColor('Build model finish!\n')
    print 'The model name is ',
    datacmdcolor.printWithColor(args.modelengineer + '\n')


    # STEP6:随机选取一只股票进行模型测试
    random.seed()
    randomnum = random.randint(1, 999999)
    while not os.path.exists(args.dirpath + "%06d" % randomnum + '.csv'):
        randomnum = random.randint(1, 999999)
    X = pd.read_csv(args.dirpath + "%06d" % randomnum + '.csv')
    X[predictcolumn + 'predict'] = IndicatorGallery.getAheadCal(X[predictcolumn], calfunc, args.interval)
    X = RefreshData.deleteRowWithNan(X)
    real_y = pd.Series(X[predictcolumn], name='real')
    predict_y = pd.Series(me.predict(X[othercolumn]), name='predict')


    lintcmdcolor.printWithColor('Test Finish!\n')
    print 'The tested stock is ',
    datacmdcolor.printWithColor("%06d" % randomnum)


    # STEP7:显示预测结果图
    dp = DrawPlot("%06d" % randomnum + ' stock predict plot')
    dp.drawLinePlot(real_y, predict_y)
    dp.drawJointPlot(real_y, predict_y)
    dp.drawDensityCurvePlot(real_y - predict_y)
