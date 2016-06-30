# Backplane

from client import webBus

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

# MREH (ASCII) = '0 77 82 69 72'
def bridgeRead(slot,address,nBytes,bus):
    herm = '0 77 82 69 72'
    bus.write(bridgeAddress(slot),[address])
    bus.read(bridgeAddress(slot),nBytes)
    batch = bus.sendBatch()
    # print 'BATCH: ',batch
    message = batch[-1]
    s = 'Slot ' + str(slot)
    if int(message[0]) != 0:
        print s + ' I2C_ERROR : ', message
        return 0
    if message != herm:
        print s + ' HERM_ERROR : ', message
        return 0
    print s + ' ACTIVE_SLOT : ', message
    return 1

def findRM(rmList,bus):
    for rm in rmList:
        print openRM(rm)
        print bridgeRead(4,0,4,bus)

def search(nGroups,bus):
    bus.write(0x72,[0x01])
    bus.read(0x72,1)
    print '0x72 = ',bus.sendBatch()
    for i in xrange(nGroups):
        byte = 2**i
        print '\n--- Write to 0x74: ',hex(byte),' = ',byte
        bus.write(0x74,[byte])
        bus.read(0x74,1)
        print '0x74 = ',bus.sendBatch()
        print 'Bridge Read = ',bridgeRead(4,0,4,bus)

class Backplane:
    def __init__(self,bus):
        self.bus = bus
        self.activeSlots = self.findActiveSlots()

    def __str__(self):
        return self.bus.address

    def openRM(self,rm):
        if rm in [3,4]:
            # Open channel to ngCCM for RM 3,4: J1 - J10
            print '### Open RM ', rm
            self.bus.write(0x72,[2])
        elif rm in [1,2]:
            # Open channel to ngCCM for RM 1,2: J17 - J26
            print '### Open RM ', rm
            self.bus.write(0x72,[1])
        else:
            print 'Invalid RM = ', rm
            print 'Please choose RM = {1,2,3,4}'
            return 'closed channel'
        # Open channel to i2c group
        self.bus.write(0x74, [ngccmGroup(rm)])
        return self.bus.sendBatch()

    def findActiveSlots(self):
        print '\nBUS = ' + str(self) + '\n'
        activeSlots = []
        for rm in [4,3,2,1]:
            self.openRM(rm)
            for slot in [1,2,3,4]:
                if bridgeRead(slot,0,4,self.bus):
                    activeSlots.append(getSlot(rm,slot))
        return activeSlots

def run(bus):
    bp = Backplane(bus)
    print '\n',str(bp),' active slots: ', bp.activeSlots, '\n'

bus5 = webBus("pi5",0)
bus6 = webBus("pi6",0)

run(bus5)
run(bus6)

# backplane6 = Backplane(bus6)
# print '\n',str(backplane6),' active slots: ',backplane6.activeSlots,'\n'
