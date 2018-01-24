#coding=utf-8
import numpy as np


class PY:
    var = ""
    def __init__(self, var):
        self.var = var


if __name__ == '__main__':
    a = PY('123')
    b = PY('456')
    print a.var, b.var