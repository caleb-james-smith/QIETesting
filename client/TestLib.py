#TestLib.py
#Testing Library for QIE Tests.

from client import webBus
import QIELib as q
b = webBus("pi5",0)

#MUX slave addresses (slave i2c addresses)
MUXs = {
    "fanout" : 0x72,
    "ngccm" : {
                "u10" : 0x74,
                "u18" : 0x70
                },
    "bridge" : [0x19, 0x1a, 0x1b, 0x1c]
        }
#Register addresses
REGs = {
    "qie0" : 0x30,
    "qie1" : 0x31,
    "iscSelect" : 0x11,
    "vttx" : 0x7E,
    "igloo" : 0x09,
    "ID" : 0x50,
    "temp" : 0x40
        }
# Simplify your life today with RMi2c and QIEi2c. Boom dog.

RMi2c = {
    # RM 0,1
    0 : 0x02, # Bit 1 = 2
    1 : 0x20, # Bit 5 = 32
    # RM 2,3
    2 : 0x10, # Bit 4 = 16
    3 : 0x01  # Bit 0 = 1
        }

QIEi2c = {
    0 : 0x19,
    1 : 0x1a,
    2 : 0x1b,
    3 : 0x1c
        }

######## Bridge Test Function Dictionary

def simplePrint(message):
    hex_message = toHex(message,1)
    print 'int message: ', message
    print 'hex message:', hex_message
    return hex_message

def passFail(result):
    if result:
        return 'PASS'
    return 'FAIL'

# Bridge Register Tests

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


bridgeDict = {
    0 : {
        'name' : 'idString',
        'function' : idString,
        'address' : 0x00,
    },
    1 : {
        'name' : 'idStringCont',
        'function' : idStringCont,
        'address' : 0x01,
    },
    2 : {
        'name' : 'fwVersion',
        'function' : fwVersion,
        'address' : 0x04,
    },
    3 : {
        'name' : 'ones',
        'function' : ones,
        'address' : 0x08,
    },
    4 : {
        'name' : 'zeroes',
        'function' : zeroes,
        'address' : 0x09,
    },
    5 : {
        'name' : 'onesZeroes',
        'function' : onesZeroes,
        'address' : 0x0A,
    },
}

# Read from I2C_SELECT device

# Read number of bytes from register for Bridge

def readRegisterBridge(slot, address, num_bytes):
    b.write(ngccmGroup(slot),[address])
    b.read(ngccmGroup(slot), num_bytes)
    message = b.sendBatch()[-1]
    return reverseBytes(message)

# Read number of bytes from register for Igloo

def readRegisterIgloo(slot, address, num_bytes):
    b.write(0x00,[0x06])
    b.write(ngccmGroup(slot),[0x11,0x03,0,0,0])
    b.write(0x09,[address])
    b.read(0x09, num_bytes)
    message = b.sendBatch()[-1]
    return reverseBytes(message)

######## open channel to RM! ######################

# Label RMs as 0, 1, 2, 3
# Label Slots as 0, 1, 2, 3
# Open Channel for QIE Card Given RM

####### happy slot things #####################

slotArray = [
    [23,24,25,26],
    [18,19,20,21],
    [7,8,9,10],
    [2,3,4,5]
]

# RM = 1,2,3,4
# Slot = 1,2,3,4
def getSlot(rm,slot):
    return slotArray[rm-1][slot-1]

# Slots 1,2,3,4
def bridgeAddress(slot):
    address = [0x19, 0x1a,0x1b, 0x1c]
    return address[slot-1]

# RMs 1,2,3,4
def ngccmGroup(rm):
    i2cGroups = [0x01,0x10,0x20,0x02]
    return i2cGroups[rm-1]


def openRM(rm):
    if rm in [3,4]:
        # Open channel to ngCCM for RM 0,1: J1 - J10
        b.write(q.MUXs["fanout"],[0x02])
    elif rm in [1,2]:
        # Open channel to ngCCM for RM 2,3: J17 - J26
        b.write(q.MUXs["fanout"],[0x01])
    else:
        print 'Invalid RM = ', rm
        print 'Please choose RM = {0,1,2,3}'
        return 'closed channel'
    # Open channel to i2c group
    b.write(q.MUXs["ngccm"]["u10"], [ngccmGroup(rm)])
    return b.sendBatch()

# Print UniqueID Arrary
# RN = Registration Number
# SN = Serial Number
def printIDs(uniqueIDArray):
    print
    for rm in xrange(len(uniqueIDArray)):
        for slot in xrange(len(uniqueIDArray[0])):
            revRN = reverseBytes(uniqueIDArray[rm][slot])
            hexRN = toHex(revRN)
            revSN = serialNum(revRN)
            hexSN = toHex(revSN)
            print 'RM: ', rm, ' slot: ', slot
            # print 'Unique Registration Number (dec): ', revRN
            # print 'Unique Registration Number (hex): ', hexRN
            # print 'Serial Number (dec): ', revSN
            print 'Serial Number (hex): ', hexSN
            print

# Split message into a list of messages. Use for QIE Dasiy Chains.
def splitMessage(message, num_parts):
    message_list = message.split()
    size = len(message_list) / num_parts
    final_message_list = []
    s = " "
    for n in xrange(num_parts):
        part_list = message_list[n*size:(n+1)*size]
        final_message_list.append(s.join(part_list))
    return final_message_list


def reverse(message):
    mList = message.split()
    mList.reverse()
    s = " "
    return s.join(mList)

# Reverse order of string of bytes separated by spaces.
# Leaves errorCode as first (leftmost) byte
def reverseBytes(message):
    mList = message.split()
    errorCode = mList.pop(0)
    mList.reverse()
    finalList = [errorCode] + mList
    s = " "
    return s.join(finalList)

def reverseKeepCRC(message):
    mList = message.split()
    errorCode = mList.pop(0)
    checksum = mList.pop()
    mList.reverse()
    finalList = [errorCode] + mList + [checksum]
    s = " "
    return s.join(finalList)

# Reverse order of string of bytes separated by spaces.
# Leaves errorCode as first (leftmost) byte.
# Leaves checksum as last (rightmost) byte.
def reverseSerial(message):
    mList = message.split()
    errorCode = mList.pop(0)
    familyCode = mList.pop(0)
    checksum = mList.pop()
    mList.reverse()
    finalList = [errorCode] + [familyCode] + mList + [checksum]
    s = " "
    return s.join(finalList)

def moveFamilyCode(message):
    mList = message.split()
    errorCode = mList.pop(0)
    familyCode = mList.pop(0)
    checksum = mList.pop()
    finalList = [errorCode] + mList + [familyCode] + [checksum]
    s = " "
    return s.join(finalList)

# reverse all bits
def reverseBits():
    return 0

# Convert string of ints to list of ints.
def toIntList(message):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = int(message_list[byte])
    return message_list

# Convert string of ints with spaces to a string of hex values with no spaces... one long string.
def toHex(message, colon=2):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = hex(int(message_list[byte]))
        message_list[byte] = message_list[byte][2:]
        if len(message_list[byte]) == 1:
            message_list[byte] = '0' + message_list[byte]
    if colon == 2:
        s = ":"
        return s.join(message_list)
    if colon == 1:
        s = " "
        return s.join(message_list)
    s = ""
    return '0x' + s.join(message_list)

# Parse Serial Number (6 bytes) from 8 byte Registration Number.
def serialNum(message):
    message_list = message.split()
    message_list = message_list[2:-1]
    s = " "
    return s.join(message_list)

#ASCII
def toASCII(message):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = chr(int(message_list[byte]))
    s = ""
    return s.join(message_list)
