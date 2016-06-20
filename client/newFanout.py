# new fanout pi6

from client import webBus
b = webBus("pi6",0)

bridgeAddress = [0x19, 0x1a,0x1b, 0x1c]

def ngccmGroup(rm):
    i2cGroups = [0x01,0x10,0x20,0x02]
    return i2cGroups[rm-1]

def openRM(rm):
    # b.write(0x00,[0x06])
    if rm in [0,1]:
        # Open channel to ngCCM for RM 0,1: J1 - J10
        print '### Open RM ', rm
        b.write(0x72,[0x02])
    elif rm in [2,3]:
        # Open channel to ngCCM for RM 2,3: J17 - J26
        print '### Open RM ', rm
        b.write(0x72,[0x01])
    else:
        print 'Invalid RM = ', rm
        print 'Please choose RM = {0,1,2,3}'
        return 'closed channel'
    # Open channel to i2c group
    b.write(0x74, [ngccmGroup(rm)])
    # b.read(0x74,1)
    # b.write(0x74, [0xFF])
    return b.sendBatch()

def bridgeRead(cardList,nBytes):
    for card in cardList:
        b.write(bridgeAddress[card],[0x0])
        b.read(bridgeAddress[card],nBytes)
    return b.sendBatch()

def findRM(rmList):
    for rm in rmList:
        print openRM(rm)
        print bridgeRead([1,3],1)

def search(nGroups):
    b.write(0x72,[0x01])
    b.read(0x72,1)
    print '0x72 = ',b.sendBatch()
    for i in xrange(nGroups):
        byte = 2**i
        print '\n--- Write to 0x74: ',hex(byte),' = ',byte
        b.write(0x74,[byte])
        b.read(0x74,1)
        print '0x74 = ',b.sendBatch()
        print 'Bridge Read = ',bridgeRead([0,1,2,3],4)

def write70(rm):
    b.write(0x72,[0x01])
    b.write(0x74,[0x08])
    b.read(0x74,1)
    print b.sendBatch()

    b.write(0x70,[0x40])
    b.write(0x70,[0x2,0xFF])
    print b.sendBatch()

    b.write(0x70,[0x40])
    b.read(0x70,2)
    print b.sendBatch()

write70(3)
search(8)
