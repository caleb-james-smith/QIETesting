from client import webBus
import caleb_checksum as cc
import TestLib as t
import QIELib as q
bus = webBus("pi5",0)

# binDataHappy = '0 01110000 00111100 10000011'
# intDataHappy = '0 112 60 131'
# value = 28732

def readTemp(slot, num_bytes, verbosity=0):
    bus.write(0x00,[0x06])
    bus.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    bus.write(0x40,[0xF3])
    bus.read(0x40, num_bytes + 1) # also read checksum byte
    message = bus.sendBatch()[-1]
    # message = intDataHappy
    value = getValue(message)
    crc = cc.checkCRC(message, 2)
    if verbosity:
        print 'message: ', message
        print 'checksum: ', crc
        print 'value: ', value
    return (crc,calcTemp(value))

def getValue(message):
    value = ''
    mList = message.split()
    mList = mList[1:-1]
    for byte in xrange(len(mList)):
        initialByte = bin(int(mList[byte]))[2:]
        length = len(initialByte)
        zeros = "".join(list('0' for i in xrange(8-length)))
        fullByte = zeros + initialByte
        value += fullByte
    value = value[:-2] + '00'
    return int(value,2)

def calcTemp(s):
    return -46.85 + 175.72 * s/2**16

def calcHumi(s):
    return -6 + 125.0 * s/2**16

def readManyTemps(rm,slot,nTemps,verbosity=0):
    t.openRM(rm)
    for i in xrange(nTemps):
        print readTemp(slot,2,verbosity)

# Set last two bits of LSB to 0 (these are status bits).
# message = '0 01100011 01010010 01100100'
# 0110'0011'0101'0000 = 25424.


# Trigger T measurement     hold master     1110'0011   0xE3
# Trigger RH measurement    hold master     1110'0101   0xE5
# Trigger T measurement     no hold master  1111'0011   0xF3
# Trigger RH measurement    no hold master  1111'0101   0xF5
