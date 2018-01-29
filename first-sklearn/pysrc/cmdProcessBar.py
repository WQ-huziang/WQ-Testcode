#!/usr/local/lib
# -*- coding: UTF-8 -*-
__author__ = 'hza'
__date__ = '2018-1-29 16:31'

import sys, time
from cmdColor import *

class CMDProcessBar():
    '显示处理进度的类'

    def __init__(self, maxstep, length=50, donesymbol='*', undonesymbol='-', barcolor=FOREGROUND_BLACK | BACKGROUND_WHITE):
        """
        构造函数
            :param self: 类变量本身
            :param maxstep: 最大步数
            :param length=50: 进度条长度
            :param donesymbol='>': 已完成的填充字符
            :param undonesymbol='-': 未完成的填充字符
        """   
        self.i = 0
        self.maxstep = maxstep
        self.length = length
        self.done = donesymbol
        self.undone = undonesymbol
        self.barcmdcolor = CMDColor(barcolor)

    def showProcess(self, i=None):
        """
        显示进度条
            :param self: 类变量本身
            :param i=None: 当前进度
        """   
        if i != None:
            self.i = i
        else:
            self.i += 1
        
        # 通过类内部信息计算进度条
        donenum = int(self.i * self.length / self.maxstep)
        undonenum = self.length - donenum #计算显示多少个'-'
        percent = self.i * 100.0 / self.maxstep #计算完成进度，格式为xx.xx%
        # \r 表示回到行首
        processbar = '\r[' + self.done * donenum + self.undone * undonenum + '] '\
                      + '%.2f' % percent + '%'
        # 输出并清空缓存
        self.barcmdcolor.printWithColor(processbar)
        sys.stdout.flush()

    def close(self, words='DONE'):
        """
        显示结束字符
            :param self: 类变量本身
            :param words='DONE': 结束字符
        """
        self.barcmdcolor.printWithColor('\n' + words)
        self.i = 0

if __name__=='__main__':
    max_steps = 100

    process_bar = CMDProcessBar(max_steps, donesymbol='>', undonesymbol='-')

    for i in range(max_steps):
        process_bar.showProcess()
        time.sleep(0.05)
    process_bar.close()