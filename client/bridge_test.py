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
    print '\n\nBRIDGE TEST\n\n'
    passed = 0
    failed = 0
    neither = 0
    for rm in RMList:
        t.openRM(rm)
        print '\n### Test RM: ', rm, ' ######'
        for slot in xrange(num_slots):
            b.write(0x00,[0x06])
            result = basicTests(slot,num_tests)
            if result == 'PASS':
                passed += 1
            elif result == 'FAIL':
                failed += 1
            else:
                print 'Neither PASS Nor FAIL'
                neither += 1
    print 'Number passed = ', passed
    print 'Number failed = ', failed
    print 'Number neither pass nor fail = ', neither, '\n'

def basicTests(slot,num_tests):
    print '## Number of Tests: ', num_tests
    for test in xrange(num_tests):
        print '\n##### Bridge Test: ', test, ' ########'
        function = t.bridgeDict[test]['function']
        address = t.bridgeDict[test]['address']
        message = t.readRegister(slot,address)
        print 'Register Value: ', message
        print 'Test Result ', function(message)
        return function(message)

##### TestLib ########

def passFail(result):
    if result:
        return 'PASS'
    return 'FAIL'

def idString(message):
    correct_value = "HERM"
    message = t.toASCII(message)
    print message
    return passFail(message==correct_value)

def idStringCont(message):
    correct_value = "Brdg"
    message = t.toASCII(message)
    print message
    return passFail(message==correct_value)

def fwVersion(message):
    correct_value = "N/A" # We need to find Firmware Version
    message = t.toHex(message)
    return message

def ones(message):
    correct_value = 0xFF
    hex_message = toHex(message)
    print hex_message
    return passFail(message==correct_value)

def zeroes(message):
    correct_value = 0x00
    hex_message = toHex(message)
    print hex_message
    return passFail(message==correct_value)

def onesZeroes(message):
    correct_value = 0xAAAAAAAA
    hex_message = toHex(message)
    print hex_message
    return passFail(message==correct_value)

runBridgeTests([0],4,6)
