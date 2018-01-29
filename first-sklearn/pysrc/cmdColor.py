#!/usr/bin/env
# -*- coding: UTF-8 -*- 
__author__ = 'hza'
__date__ = '2018-1-29 15:11'

import ctypes
import sys

# stdin, stdout, stderr 三种模式
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# Windows CMD命令行 字体颜色定义 text colors
FOREGROUND_BLACK = 0x00 # black.
FOREGROUND_DARKBLUE = 0x01 # dark blue.
FOREGROUND_DARKGREEN = 0x02 # dark green.
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
FOREGROUND_DARKRED = 0x04 # dark red.
FOREGROUND_DARKPINK = 0x05 # dark pink.
FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
FOREGROUND_DARKWHITE = 0x07 # dark white.
FOREGROUND_DARKGRAY = 0x08 # dark gray.
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_SKYBLUE = 0x0b # skyblue.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_PINK = 0x0d # pink.
FOREGROUND_YELLOW = 0x0e # yellow.
FOREGROUND_WHITE = 0x0f # white.
 
# Windows CMD命令行 背景颜色定义 background colors
BACKGROUND_BLACK = 0x00 # black
BACKGROUND_BLUE = 0x10 # dark blue.
BACKGROUND_GREEN = 0x20 # dark green.
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
BACKGROUND_DARKRED = 0x40 # dark red.
BACKGROUND_DARKPINK = 0x50 # dark pink.
BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
BACKGROUND_DARKWHITE = 0x70 # dark white.
BACKGROUND_DARKGRAY = 0x80 # dark gray.
BACKGROUND_BLUE = 0x90 # blue.
BACKGROUND_GREEN = 0xa0 # green.
BACKGROUND_SKYBLUE = 0xb0 # skyblue.
BACKGROUND_RED = 0xc0 # red.
BACKGROUND_PINK = 0xd0 # pink.
BACKGROUND_YELLOW = 0xe0 # yellow.
BACKGROUND_WHITE = 0xf0 # white.

# 标准命令行
stdinhandle = ctypes.windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)
stdouthandle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
stderrhandle = ctypes.windll.kernel32.GetStdHandle(STD_ERROR_HANDLE)

class CMDColor:
    '设置cmd命令行颜色'

    def __init__(self, color):
        """
        构造函数
            :param self: 类变量本身
            :param color: 颜色
        """
        self.color = color

    def setCmdTextColor(self, handle=stdouthandle):
        """
        设置颜色，可以同时设置字体和背景颜色，通过|
            :param self: 类变量本身
            :param color: 颜色
            :param handle=stdouthandle: 输入输出接口
            :returns: 是否成功
        """
        return ctypes.windll.kernel32.SetConsoleTextAttribute(handle, self.color)

    def resetColor(self, handle=stdouthandle):
        """
        回复原先颜色
            :param self: 类变量本身
            :param handle=stdouthandle: 输入输出接口
        """   
        return ctypes.windll.kernel32.SetConsoleTextAttribute(handle, FOREGROUND_DARKWHITE)

    def printWithColor(self, mess):
        """
        输出颜色
            :param self: 类变量本身
            :param mess: 输出信息
        """
        self.setCmdTextColor()
        sys.stdout.write(mess)
        self.resetColor()

if __name__ == '__main__':
    CMDColor.setCmdTextColor(FOREGROUND_RED | BACKGROUND_YELLOW)
    print 'I am BLUE???'
    print 'REALLY???'
    self.resetColor()
    print 'goback?'
