from client import webBus
# import QIELib
import TestLib
b = webBus("pi5",0)
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
            b.write(0x00,[0x06])
            basicTests(slot,num_tests)

def basicTests(slot,num_tests):
    for test in xrange(num_tests):
        print 'Bridge Test: ', test
        function = t.bridgeDict[test]['function']
        address = t.bridgeDict[test]['address']
        message = t.readRegister(slot,address)
        print 'Register Value: ', message
        print 'Test Result ', function(message)

##### TestLib ########

def passFail(result):
    if result:
        return 'PASS'
    return 'FAIL'

def idString(message):
    correct_value = "HERM"
    return passFail(message==correct_value)

def idStringCont(message):
    correct_value = "Brdg"
    return passFail(message==correct_value)

def fwVersion(message):
    correct_value = "N/A"
    return passFail(message)

def ones(message):
    correct_value = 0xFF
    return passFail(message==correct_value)

def zeroes(message):
    correct_value = 0x00
    return passFail(message==correct_value)

def onesZeroes(message):
    correct_value = 0xAAAAAAAA
    return passFail(message==correct_value)

runBridgeTests([0],4,6)
