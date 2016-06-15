from client import webBus
import TestLib as t
b = webBus("pi5")

def test(rmList):
    for rm in rmList:
        print t.openRM(rm)

test([0,1,2,3])
