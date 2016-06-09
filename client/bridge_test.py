from client import webBus
# import QIELib
import TestLib
b = webBus("pi5")
# q = QIELib
t = TestLib

def bridge0(rm,slot):
    t.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x00])
    b.read(q.QIEi2c[slot],4)
    return b.sendBatch()[-1]

def read_qie_reg():
    b.write(q.QIEi2c[slot],[0x00])

# print bridge(0,0)

# Bridge Register Tests

def basicBridgeTests(num_tests):
    for n in xrange(num_tests):
        function = bridgeDict[n]['function']
        address = bridgeDict[n]['address']


def idString(rm,slot,address):
    address = bridgeDict[index]['address']

def idStringCont():

def fwVersion():

def ones():

def zeroes():

def onesZeroes():
