#coding=utf-8
# main文档

def test(a):
    print a(1, 2)

if __name__ == '__main__':
    test(lambda x,y: x +y)