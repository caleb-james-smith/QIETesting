# Run complete QIE Test Sweet
from client import webBus
import uniqueID
import TestLib
b = webBus("pi5")
u = uniqueID
t = TestLib

def run(RMList, num_slots=4):
    uniqueIDArray = []
    # Iterate through RM 0, 1, 2, 3 (include desired RMs in list)
    for rm in RMList:
        idList = []
        # Iterate through Slot 0, 1, 2, 3 (run for all 4 slots by default)
        for slot in xrange(num_slots):
            idList.append(u.uniqueID(rm,slot))
            # b.clearBus()
        uniqueIDArray.append(idList)
    return uniqueIDArray

### Outdated, not used now! ###
def printRun(RMList, num_slots=4):
    uniqueIDArray = run(RMList, num_slots)
    for rm in RMList:
        for slot in xrange(num_slots):
            print 'RM: ', rm, ' slot: ', slot
            print 'UniqueID (dec): ', t.reverseBytes(uniqueIDArray[rm][slot])
            print 'UniqueID (hex): ', t.toHex(t.reverseBytes(uniqueIDArray[rm][slot]))

# Use printIDs from TestLib
uniqueIDArray = run([0])
t.printIDs(uniqueIDArray)

# That output, though? It's Greek to me!
