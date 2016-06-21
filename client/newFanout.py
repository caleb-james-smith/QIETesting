# new fanout pi6

from client import webBus
b = webBus("pi6",0)
bus5 = webBus("pi5",0)
bus6 = webBus("pi6",0)

# Slots 1,2,3,4
def bridgeAddress(slot):
    address = [0x19, 0x1a,0x1b, 0x1c]
    return address[slot-1]

# RMs 1,2,3,4
def ngccmGroup(rm):
    i2cGroups = [0x01,0x10,0x20,0x02]
    return i2cGroups[rm-1]

def openRM(rm,bus):
    if rm in [3,4]:
        # Open channel to ngCCM for RM 3,4: J1 - J10
        print '### Open RM ', rm
        bus.write(0x72,[2])
    elif rm in [1,2]:
        # Open channel to ngCCM for RM 1,2: J17 - J26
        print '### Open RM ', rm
        bus.write(0x72,[1])
    else:
        print 'Invalid RM = ', rm
        print 'Please choose RM = {1,2,3,4}'
        return 'closed channel'
    # Open channel to i2c group
    bus.write(0x74, [ngccmGroup(rm)])
    return bus.sendBatch()

def bridgeRead(cardList,nBytes,bus):
    for card in cardList:
        bus.write(bridgeAddress(card),[0x0])
        bus.read(bridgeAddress(card),nBytes)
    return bus.sendBatch()

def findRM(rmList):
    for rm in rmList:
        print openRM(rm)
        print bridgeRead([2,4],1)

def search(nGroups,bus):
    bus.write(0x72,[0x01])
    bus.read(0x72,1)
    print '0x72 = ',b.sendBatch()
    for i in xrange(nGroups):
        byte = 2**i
        print '\n--- Write to 0x74: ',hex(byte),' = ',byte
        bus.write(0x74,[byte])
        bus.read(0x74,1)
        print '0x74 = ',bus.sendBatch()
        print 'Bridge Read = ',bridgeRead([1,2,3,4],4,bus)

def write70(bus):
    bus.write(0x72,[0x01])
    bus.write(0x74,[0x08])
    bus.read(0x74,1)
    print bus.sendBatch()

    bus.read(0x70,1)
    print bus.sendBatch()

    bus.write(0x70,[3,0])
    bus.write(0x70,[1,0])
    print bus.sendBatch()

def readClock(rm,slot,nReads,bus):
    openRM(rm,bus)
    address = bridgeAddress(slot)
    for i in xrange(nReads):
        bus.write(address,[0x12])
        bus.read(address,4)
        print bus.sendBatch()

# write70(bus6)
# openRM(1)
# search(8,bus6)
readClock(1,4,20,bus6)
