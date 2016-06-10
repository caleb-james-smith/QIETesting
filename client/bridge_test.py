from client import webBus
# import QIELib
import TestLib
b = webBus("pi5")
# q = QIELib
t = TestLib

def bridge0(rm,slot):
    t.openRM(rm)
    b.write(q.QIEi2c[slot],[0x00])
    b.read(q.QIEi2c[slot],4)
    return b.sendBatch()[-1]

def read_qie_reg():
    b.write(q.QIEi2c[slot],[0x00])

# print bridge(0,0)

# Bridge Register Tests

def runBridgeTests(RMList,num_slots,num_tests):
    for rm in RMList:
        t.openRM(rm)
        print 'Test RM: ', rm
        for slot in xrange(num_slots):
            b.write(0x00,0x06)
            basicTests(slot,num_tests)

def basicTests(slot,num_tests):
    for test in xrange(num_tests):
        print 'Bridge Test: ', test
        function = t.bridgeDict[n]['function']
        address = t.bridgeDict[n]['address']
        message = t.readRegister(slot,address)
        print 'Register Value: ', message
        print 'Test Result ', t.function(message)

runBridgeTests([0],4,6)
