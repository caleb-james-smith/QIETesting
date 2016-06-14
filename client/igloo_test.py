from client import webBus
from operator import add
import TestLib as t
import QIELib as q
b = webBus("pi5")

# Examlpe for register address 0x00
def igloo0(rm,slot):
    t.openRM(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
    b.write(0x09,[0x00])
    b.read(0x09,8)
    return b.sendBatch()[-1]

# Adry's open Igloo function
def openIgloo(rm,slot):
    t.openRM(rm,slot)
    #the igloo is value "3" in I2C_SELECT table
    b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
    b.sendBatch()

############### Igloo Register Tests #############################

def runIglooTests(RMList, num_slots, num_tests, verbosity=0):
    print '\n\nBRIDGE TEST\n\n'
    total_passed = 0
    total_failed = 0
    total_neither = 0
    total_number_tests = num_slots * num_tests
    total_test_list = [total_passed, total_failed, total_neither]
    for rm in RMList:
        t.openRM(rm)
        print '\n-------------------- Test RM: ', rm, ' --------------------'
        for slot in xrange(num_slots):
            # Reset all devices!
            b.write(0x00,[0x06]) # also present in readRegisterIgloo.
            print '\n-------------------- Test Slot: ', slot, ' --------------------'
            test_list = iglooTests(slot,num_tests)
            total_test_list = map(add, total_test_list, test_list)
            # daisyChain = q.qCard(webBus("pi5",0), q.QIEi2c[slot])
            # print '\n~~~~~~~~~~ QIE Daisy Chain ~~~~~~~~~~'
            # print str(daisyChain)
            if verbosity:
                print '\nNumber passed = ', test_list[0]
                print 'Number failed = ', test_list[1]
                print 'Number neither pass nor fail = ', test_list[2], '\n'

    # Print Final Test Results for Bridge FPGA
    print '\n\n########   Final Test Results  ########\n'
    print 'Total Number of Tests = ', total_number_tests
    print 'Number passed = ', total_test_list[0]
    print 'Number failed = ', total_test_list[1]
    print 'Number neither pass nor fail = ', total_test_list[2]
    print 'Check total number of tests: ', total_number_tests == sum(total_test_list), '\n'

def iglooTests(slot, num_tests, verbosity=0):
    passed = 0
    failed = 0
    neither = 0
    print '## Number of Tests: ', num_tests
    for test in xrange(num_tests):
        print '\n### Igloo Test: ', test, ' ###'
        print '\n### Test Name: ', iglooDict[test]['name']
        function = iglooDict[test]['function']
        address = iglooDict[test]['address']
        num_bytes = iglooDict[test]['bits']/8
        message = t.readRegisterIgloo(slot, address, num_bytes)
        result = function(message)
        if result == 'PASS':
            passed += 1
        elif result == 'FAIL':
            failed += 1
        else:
            print 'Neither PASS Nor FAIL'
            neither += 1
        if verbosity:
            print 'Register Name: ', iglooDict[test]['name']
            print 'Register Value: ', message
            print 'Test Result: ', result

    test_list = [passed, failed, neither]
    return test_list

############ Igloo Registers #############

iglooDict = {
    0 : {
        'name' : 'FPGA_MAJOR_VERSION',
        # 'function' : majorVersion,
        'function' : t.simplePrint,
        'address' : 0x00,
        'bits' : 8,
        'write' : False
    },
    1 : {
        'name' : 'FPGA_MINOR_VERSION',
        # 'function' : minorVersion,
        'function' : t.simplePrint,
        'address' : 0x01,
        'bits' : 8,
        'write' : False
    },
    2 : {
        'name' : 'OnesRegister',
        # 'function' : onesRegister,
        'function' : t.simplePrint,
        'address' : 0x02,
        'bits' : 32,
        'write' : False
    },
    3 : {
        'name' : 'ZerosRegister',
        # 'function' : zerosRegister,
        'function' : t.simplePrint,
        'address' : 0x03,
        'bits' : 32,
        'write' : False
    },
    4 : {
        'name' : 'FPGA_TopOrBottom',
        # 'function' : topOrBottom,
        'function' : t.simplePrint,
        'address' : 0x04,
        'bits' : 8,
        'write' : False
    },
    5 : {
        'name' : 'UniqueID',
        # 'function' : writeUniqueID,
        'function' : t.simplePrint,
        'address' : 0x05,
        'bits' : 8,
        'write' : True
    },
    6 : {
        'name' : 'StatusReg',
        # 'function' : statusReg,
        'function' : t.simplePrint,
        'address' : 0x10,
        'bits' : 8,
        'write' : False
    },
    7 : {
        'name' : 'CntrReg',
        # 'function' : cntrReg,
        'function' : t.simplePrint,
        'address' : 0x11,
        'bits' : 32,
        'write' : False
    },
    8 : {
        'name' : 'Clk_count',
        # 'function' : clkCount,
        'function' : t.simplePrint,
        'address' : 0x12,
        'bits' : 32,
        'write' : False
    },
    9 : {
        'name' : 'RST_QIE_count',
        # 'function' : rstQIECount,
        'function' : t.simplePrint,
        'address' : 0x13,
        'bits' : 32,
        'write' : False
    },
    10 : {
        'name' : 'WTE_count',
        # 'function' : wteCount,
        'function' : t.simplePrint,
        'address' : 0x14,
        'bits' : 32,
        'write' : False
    },
    11 : {
        'name' : 'CapIdErrLink1_count',
        # 'function' : CapIdErr1,
        'function' : t.simplePrint,
        'address' : 0x15,
        'bits' : 32,
        'write' : False
    },
    12 : {
        'name' : 'CapIdErrLink2_count',
        # 'function' : CapIdErr2,
        'function' : t.simplePrint,
        'address' : 0x16,
        'bits' : 32,
        'write' : False
    },
    13 : {
        'name' : 'CapIdErrLink3_count',
        # 'function' : CapIdErr3,
        'function' : t.simplePrint,
        'address' : 0x17,
        'bits' : 32,
        'write' : False
    },
    14 : {
        'name' : 'fifo_data_1',
        # 'function' : fifoData1,
        'function' : t.simplePrint,
        'address' : 0x30,
        'bits' : 88,
        'write' : False
    },
    15 : {
        'name' : 'fifo_data_2',
        # 'function' : fifoData2,
        'function' : t.simplePrint,
        'address' : 0x31,
        'bits' : 88,
        'write' : False
    },
    16 : {
        'name' : 'fifo_data_3',
        # 'function' : fifoData3,
        'function' : t.simplePrint,
        'address' : 0x32,
        'bits' : 88,
        'write' : False
    },
    17 : {
        'name' : 'InputSpy',
        # 'function' : inputSpy,
        'function' : t.simplePrint,
        'address' : 0x33,
        'bits' : 200,
        'write' : False
    },
    18 : {
        'name' : 'Spy96bits',
        # 'function' : spy96,
        'function' : t.simplePrint,
        'address' : 0x40,
        'bits' : 96,
        'write' : False
    },
    19 : {
        'name' : 'QieClockPhase1',
        # 'function' : qieClockPhase1,
        'function' : t.simplePrint,
        'address' : 0x60,
        'bits' : 8,
        'write' : True
    },
    20 : {
        'name' : 'QieClockPhase2',
        # 'function' : qieClockPhase2,
        'function' : t.simplePrint,
        'address' : 0x61,
        'bits' : 8,
        'write' : True
    },
    21 : {
        'name' : 'QieClockPhase3',
        # 'function' : qieClockPhase3,
        'function' : t.simplePrint,
        'address' : 0x62,
        'bits' : 8,
        'write' : True
    },
    22 : {
        'name' : 'QieClockPhase4',
        # 'function' : qieClockPhase4,
        'function' : t.simplePrint,
        'address' : 0x63,
        'bits' : 8,
        'write' : True
    },
    23 : {
        'name' : 'QieClockPhase5',
        # 'function' : qieClockPhase5,
        'function' : t.simplePrint,
        'address' : 0x64,
        'bits' : 8,
        'write' : True
    },
    24 : {
        'name' : 'QieClockPhase6',
        # 'function' : qieClockPhase6,
        'function' : t.simplePrint,
        'address' : 0x65,
        'bits' : 8,
        'write' : True
    },
    25 : {
        'name' : 'QieClockPhase7',
        # 'function' : qieClockPhase7,
        'function' : t.simplePrint,
        'address' : 0x66,
        'bits' : 8,
        'write' : True
    },
    26 : {
        'name' : 'QieClockPhase8',
        # 'function' : qieClockPhase8,
        'function' : t.simplePrint,
        'address' : 0x67,
        'bits' : 8,
        'write' : True
    },
    27 : {
        'name' : 'QieClockPhase9',
        # 'function' : qieClockPhase9,
        'function' : t.simplePrint,
        'address' : 0x68,
        'bits' : 8,
        'write' : True
    },
    28 : {
        'name' : 'QieClockPhase10',
        # 'function' : qieClockPhase10,
        'function' : t.simplePrint,
        'address' : 0x69,
        'bits' : 8,
        'write' : True
    },
    29 : {
        'name' : 'QieClockPhase11',
        # 'function' : qieClockPhase11,
        'function' : t.simplePrint,
        'address' : 0x6A,
        'bits' : 8,
        'write' : True
    },
    30 : {
        'name' : 'QieClockPhase12',
        # 'function' : qieClockPhase12,
        'function' : t.simplePrint,
        'address' : 0x6B,
        'bits' : 8,
        'write' : True
    },
    31 : {
        'name' : 'link_test_mode',
        # 'function' : linkTestMode,
        'function' : t.simplePrint,
        'address' : 0x80,
        'bits' : 8,
        'write' : True
    },
    32 : {
        'name' : 'link_test_mode',
        # 'function' : linkTestMode,
        'function' : t.simplePrint,
        'address' : 0x80,
        'bits' : 8,
        'write' : True
    },
    33 : {
        'name' : 'link_test_pattern',
        # 'function' : linkTestPattern,
        'function' : t.simplePrint,
        'address' : 0x81,
        'bits' : 32,
        'write' : True
    },
    34 : {
        'name' : 'DataToSERDES',
        # 'function' : dataToSERDES,
        'function' : t.simplePrint,
        'address' : 0x82,
        'bits' : 32,
        'write' : True
    },
    35 : {
        'name' : 'AddrToSERDES',
        # 'function' : addrToSERDES,
        'function' : t.simplePrint,
        'address' : 0x83,
        'bits' : 16,
        'write' : True
    },
    36 : {
        'name' : 'CtrlToSERDES',
        # 'function' : ctrlToSERDES,
        'function' : t.simplePrint,
        'address' : 0x84,
        'bits' : 8,
        'write' : True
    },
    37 : {
        'name' : 'DataFromSERDES',
        # 'function' : dataFromSERDES,
        'function' : t.simplePrint,
        'address' : 0x85,
        'bits' : 32,
        'write' : True
    },
    38 : {
        'name' : 'StatFromSERDES',
        # 'function' : statFromSERDES,
        'function' : t.simplePrint,
        'address' : 0x86,
        'bits' : 16,
        'write' : True
    },
    39 : {
        'name' : 'ScratchReg',
        # 'function' : scratchReg,
        'function' : t.simplePrint,
        'address' : 0x87,
        'bits' : 32,
        'write' : True
    }
}

# runIglooTests(RMList, num_slots, num_tests, verbosity=0)
runIglooTests([0],4,40)
