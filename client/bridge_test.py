from client import webBus
from operator import add
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
    total_passed = 0
    total_failed = 0
    total_neither = 0
    total_test_list = [total_passed, total_failed, total_neither]
    for rm in RMList:
        t.openRM(rm)
        print '\n### Test RM: ', rm, ' ######'
        for slot in xrange(num_slots):
            b.write(0x00,[0x06])
            test_list = basicTests(slot,num_tests)
            test_list = map(add, total_test_list, test_list)
            print 'Number passed = ', test_list[0]
            print 'Number failed = ', test_list[1]
            print 'Number neither pass nor fail = ', test_list[2], '\n'

    print '\n\n########   Final Test Results  ########\n\n'
    print 'Number passed = ', total_test_list[0]
    print 'Number failed = ', total_test_list[1]
    print 'Number neither pass nor fail = ', total_test_list[2], '\n'

def basicTests(slot,num_tests):
    passed = 0
    failed = 0
    neither = 0
    print '## Number of Tests: ', num_tests
    for test in xrange(num_tests):
        print '\n##### Bridge Test: ', test, ' ########'
        function = t.bridgeDict[test]['function']
        address = t.bridgeDict[test]['address']
        message = t.readRegister(slot,address)
        result = function(message)
        if result == 'PASS':
            passed += 1
        elif result == 'FAIL':
            failed += 1
        else:
            print 'Neither PASS Nor FAIL'
            neither += 1

        print 'Register Value: ', message
        print 'Test Result: ', result
    test_list = [passed, failed, neither]
    return test_list

##### TestLib ########

def passFail(result):
    if result:
        return 'PASS'
    return 'FAIL'

def idString(message):
    correct_value = "HERM"
    message = t.toASCII(message)
    print 'correct value: ',correct_value
    print 'message: ', message
    return passFail(message==correct_value)

def idStringCont(message):
    correct_value = "Brdg"
    message = t.toASCII(message)
    print 'correct value: ',correct_value
    print 'message: ', message
    return passFail(message==correct_value)

def fwVersion(message):
    correct_value = "N/A" # We need to find Firmware Version
    message = t.toHex(message)
    print 'correct value: ',correct_value
    print 'message: ', message
    return message

def ones(message):
    correct_value = 0xFF
    hex_message = toHex(message)
    print hex_message
    print 'correct value: ',correct_value
    print 'message: ', message
    return passFail(message==correct_value)

def zeroes(message):
    correct_value = 0x00
    hex_message = toHex(message)
    print hex_message
    print 'correct value: ',correct_value
    print 'message: ', message
    return passFail(message==correct_value)

def onesZeroes(message):
    correct_value = 0xAAAAAAAA
    hex_message = toHex(message)
    print hex_message
    print 'correct value: ',correct_value
    print 'message: ', message
    return passFail(message==correct_value)

runBridgeTests([0],4,6)
