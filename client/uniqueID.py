# Read UniqueID from QIE Card
from client import webBus
import TestLib as t
from caleb_checksum import checkCRC
b = webBus("pi5",0)

# Read UniqueID 8 bytes from SSN, U48 on QIE Card
def uniqueID(slot):
    # Reset entire board by writing 0x6 to 0x0.
    b.write(0x00,[0x06])
    # Note that the i2c_select has register address 0x11
    # Value : 4 = 0x04 selects 0x50
    # Note that the SSN expects 32 bits (4 bytes) for writing (send 0x4, 0, 0, 0)
    b.write(t.QIEi2c[slot],[0x11,0x04,0,0,0])
    # Send 0x0 to 0x50 in order to set pointer for reading ID
    # This removes the permutation problem!
    b.write(0x50,[0x00])
    b.read(0x50,8)
    raw_message = b.sendBatch()[-1]
    return t.reverseBytesCRC(raw_message)

# Read UniqueID for all QIE Cards in Backplane
# To read IDs for RM 1, pass RMList = [0]
# To read IDs for all RMS, pass RMList = [0, 1, 2, 3]
def getUniqueIDs(rmList, slotList, verbose=0):
    uniqueIDArray = []
    # Iterate through RM 0, 1, 2, 3 (include desired RMs in list)
    for rm in rmList:
        t.openRM(rm)
        idList = []
        # Iterate through Slot 0, 1, 2, 3 (run for all 4 slots by default)
        for slot in slotList[rm]:
            message = uniqueID(slot)
            print checkCRC(message,7,10,1)
            idList.append(message)
        uniqueIDArray.append(idList)
        print 'RM ',rm
        print idList
    return uniqueIDArray

rmList = [3,0] # Run RM 3 tests, then run RM 0 tests
slotList = [ [0,3], 0, 0, [1,2,3] ]
print getUniqueIDs(rmList, slotList, 0)
