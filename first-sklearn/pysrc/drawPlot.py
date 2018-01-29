#!/usr/bin/env
# -*- coding: UTF-8 -*- 
__author__ = 'hza'
__date__ = '2018-1-28 15:06'

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DrawPlot:
    '用于画图表的类'

    def __init__(self, title='Plot', lineweight=0.5, linecolors=['navy', 'red', 'green']):
        """
        初始化函数
            :param self: 类变量本身 
            :param title='Plot': 图的名字
            :param lineweight=0.5: 线的粗细度
            :param linecolors=['navy','red','green']: 线的颜色列表，列表长度必须不小于3
        """   
        if len(linecolors) < 3:
            raise Exception('The size of variable \'linecolors\' must larger then 2')
        self.title = title
        self.lineweight = lineweight
        self.linecolors = linecolors

    def drawLinePlot(self, se1, se2):
        """
        画线性图，图中包含序列1的value值，序列2的value值，序列1-序列2的value值，用于比较。
            :param self: 类变量本身
            :param se1: 序列1
            :param se2: 序列2
        """
        if not (se1.index == se2.index).all():
            raise Exception('predict\'s index isn\'t equal real\'s index!')
        index = se1.index
        plt.title(self.title)
        plt.plot(index, se1, color=self.linecolors[0], lw=self.lineweight, label=se1.name)
        plt.plot(index, se2, color=self.linecolors[1], lw=self.lineweight, label=se2.name)
        plt.xlabel('Index')  
        plt.ylabel('Value')
        plt.legend()
        plt.show()

    def drawJointPlot(self, se1, se2):
        """
        画线性相关图，表示序列1和序列2的相关性
            :param self: 类变量本身
            :param se1: 序列1
            :param se2: 序列2
        """   
        sns.jointplot(se1, se2, kind='reg', color=self.linecolors[0])
        # plt.title(self.title)
        plt.legend()
        plt.show()

    def drawDensityCurvePlot(self, se):
        """
        画密度曲线图，表示序列的密度曲线（即直方图）
            :param self: 类变量本身
            :param se: 序列
        """   
        sns.distplot(se, kde=True, color=self.linecolors[0])
        plt.title(self.title)
        plt.xlabel('Difference')
        plt.ylabel('Percentage')          
        plt.legend()
        plt.show()

if __name__ == '__main__':
    df = pd.read_csv('../data/5min/000001.csv')
    
    # 测试DrawPlot类
    dplot = DrawPlot()
    #dplot.drawLinePlot(df['open'], df['close'])
    #dplot.drawJointPlot(df['open'], df['close'])
    dplot.drawDensityCurvePlot(df['open'] - df['close'])
