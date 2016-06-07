# Run complete QIE Test Sweet
from client import webBus
import uniqueID
b = webBus("pi5")
u = uniqueID

def run(RMList):
    uniqueIDArray = range(4)
    num_slots = 1
    # Iterate through RM 0, 1, 2, 3 (include desired RMs in list)
    for rm in RMList:
        idList = range(num_slots)
        # Iterate through Slot 0, 1, 2, 3 (run for all 4 slots by default)
        for slot in range(num_slots):
            idList[slot] = u.uniqueID(rm,slot)
            b.clearBus()
        uniqueIDArray[rm] = idList
    return uniqueIDArray

def printRun(RMList):
    uniqueIDArray = run(RMList)
    num_slots = 1
    for rm in RMList:
        for slot in range(num_slots):
            print 'RM: ', rm, ' slot: ', slot
            print 'UniqueID: ', uniqueIDArray[rm][slot]

printRun([0])
