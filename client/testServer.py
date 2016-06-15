from client import webBus
import TestLib as t
b = webBus("pi5")

def test(rmList):
    for rm in rmList:
        print t.openRM(rm)
        b.read(0x74,1)
        print b.sendBatch()

# test([0])
b.write(1111,[1])
