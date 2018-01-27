#!/usr/bin/env
# -*- coding: UTF-8 -*- 
__author__ = 'hza'
__date__ = '2018-1-26 15:27'

import numpy as np
import pandas as pd

class IndicatorGallery:
    '数据指标库类，用于计算Series列的各种指标'
    '此类为静态类'

    @staticmethod
    def _calEMA(N, a, b):
        """
        辅助函数，计算EMA的值。
            :param N: 第N项
            :param a: close_price_today
            :param b: ema_yesterday
            :returns: EMA值
        """   
        return 2 / float(N + 1) * (a - b) + b

    @staticmethod
    def getNext(series):
        """
        得到该序列的下一个时刻序列，即将序列上移一位。
            :param series: 输入序列
            :returns: 新的序列
        """
        return IndicatorGallery.getAheadData(series, 1)

    @staticmethod
    def getAheadData(series, interval=10):
        """
        得到该序列的下interval个时刻序列，即将序列上移interval位。
            :param series: 输入序列
            :param interval=10: 时序
            :returns: 新的序列 
        """
        return series.shift(-interval)

    @staticmethod
    def getAheadAvg(series, interval=10):
        """
        得到该序列接下来interval个值的平均值，数据自己本身不算在内，如果数据量不够，赋为nan。
            :param series: 输入序列
            :param interval=10: 时序 
            :returns: 新的序列 
        """   
        return IndicatorGallery.getAheadCal(series, np.average, interval)

    @staticmethod
    def getAheadMin(series, interval=10):
        """
        得到该序列接下来interval个值的最小值，数据自己本身不算在内，如果数据量不够，赋为nan。
            :param series: 输入序列
            :param interval=10: 时序 
            :returns: 新的序列 
        """   
        return IndicatorGallery.getAheadCal(series, np.min, interval)

    @staticmethod
    def getAheadMax(series, interval=10):
        """
        得到该序列接下来interval个值的最大值，数据自己本身不算在内，如果数据量不够，当赋为nan。
            :param series: 输入序列
            :param interval=10: 时序 
            :returns: 新的序列 
        """   
        return IndicatorGallery.getAheadCal(series, np.max, interval)

    @staticmethod
    def getAheadSum(series, interval=10):
        """
        得到该序列接下来interval个值的总和，数据自己本身不算在内，如果数据量不够，当赋为nan。
            :param series: 输入序列
            :param interval=10: 时序 
            :returns: 新的序列 
        """   
        return IndicatorGallery.getAheadCal(series, np.sum, interval)

    @staticmethod
    def getAheadCal(series, func, interval=10):
        """
        得到该序列接下来interval个值，并用给定的函数进行运算，返回运算结果序列。
        数据自己本身不算在内，如果数据量不够，当赋为nan。
            :param series: 输入序列
            :param func: 给定函数，要求符合 func :: np.Serial -> digit Object
            :param interval=10: 时序 
            :returns: 新的序列 
        """
        return IndicatorGallery.getAheadCalWithFilter(series, func, lambda x : True, [], interval)

    @staticmethod
    def getAheadCalWithFilter(series, calfunc, filterfunc, filterfuncparams, interval=10):
        """
        得到该序列接下来interval个值，先用给定的过滤函数对数据进行过滤，再用给定的运算函数进行运算，返回运算结果序列。
        数据自己本身不算在内，如果数据量不够，当赋为nan。
            :param series: 输入序列
            :param calfunc: 给定运算函数，要求符合 calfunc :: np.Serial -> digit Object
            :param filterfunc: 给定过滤函数，要求符合 filterfun :: filterfuncparams -> index -> True/False，如果返回结果为False，赋为nan
            :param filterfuncparams: 过滤函数的参数，真正传入函数时，参数会加上index（代表处理数据的下标）
            :param interval=10: 时序
            :returns: 新的序列
        """   
        datalist = []
        for index in range(len(series)):
            if index + interval + 1 >= len(series):
                datalist.append(np.nan)
                continue
            if filterfunc(*(filterfuncparams + [index])):
                datalist.append(calfunc(list(series[index + 1:index + interval + 1])))
            else:
                datalist.append(np.nan)
        return pd.Series(datalist)

    @staticmethod
    def getMACD(series, short=12, llong=26, diff=9):
        """
        计算该列MACD的值。
        MACD[i + 1] = 2 * a * (emashort[i + 1] - emalong[i + 1] - MACD[i]) - MACD[i]
            :param self: 类变量本身
            :param short=12: short ema的a值，一般为12
            :param llong=26: long ema的a值，一般为26
            :param diff=9: diff的a值，一般为9
        """   
        se_macd = []
        # 初始化第一个值
        emashort, emalong = series[0], series[0]
        se_macd.append(emashort - emalong)
        # 递归计算MACD
        for i in range(len(series))[1:]:
            emashort = IndicatorGallery._calEMA(short, series[i], emashort)
            emalong = IndicatorGallery._calEMA(llong, series[i], emalong)
            se_macd.append(IndicatorGallery._calEMA(diff, 2 * (emashort - emalong), se_macd[i - 1]))
        return pd.Series(se_macd)

if __name__ == "__main__":
    df = pd.read_csv('../data/1day/000001.csv')
    del df['date']
    
    # 测试IndicatorGallery类
    series = df['close']
    IndicatorGallery.getNext(series)
    IndicatorGallery.getAheadData(series)
    IndicatorGallery.getAheadMin(series)
    IndicatorGallery.getAheadMax(series)
    IndicatorGallery.getAheadAvg(series)
    IndicatorGallery.getAheadSum(series)
    IndicatorGallery.getMACD(series)
    IndicatorGallery.getAheadCal(series, lambda x: x)
    IndicatorGallery.getAheadCalWithFilter(series, lambda x: x, lambda df, col, index: df.iloc[index][col] > 0, [df, 'price_change'])