# It is time to check your sum!
# CRC = Cyclic Redundancy Check

import collections
import Format as f

# Convert string of ints to list of ints.
def toIntList(message, base=10):
    mList = message.split()
    for byte in xrange(len(mList)):
        mList[byte] = int(mList[byte], base)
    return mList

# Check Sum function from Temp/Humi Documentation.
def checkCRC(message, numBytes, base=10, verbose=0):
    POLYNOMIAL = 0x131 # x^8 + x^5 + x^4 + 1 -> 9'b100110001 = 0x131
    crc = 0
    mList = toIntList(message, base)
    errorCode = mList[0]
    dataList = mList[1:-1]
    checksum = mList[-1]
    if errorCode != 0:
        print 'I2C_BUS_ERROR'
        return False
    # calculates 8-bit checksum with give polynomial
    for byteCtr in xrange(numBytes):
        crc ^= dataList[byteCtr]
        if verbose > 1:
            print "CRC = ",crc
        for bit in xrange(8,0,-1):
            if crc & 0x80: # True if crc >= 128, False if crc < 128
                crc = (crc << 1) ^ POLYNOMIAL
                if verbose > 1:
                    print 'true crc = ',crc
            else: # crc < 128
                crc = (crc << 1)
                if verbose > 1:
                    print 'false crc = ',crc
    if verbose > 0:
        print 'CRC = ',crc
        print 'checksum = ',checksum
    if crc != checksum:
        if verbose > 0:
            print 'CHECKSUM_ERROR'
        return False
    if verbose > 0:
        print 'CHECKSUM_OK'
    return True
