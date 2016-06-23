# Check Checsum!!

from checksumClass import Checksum
from uniqueIDClass import ID
import TestLib as t
from client import webBus
bus6 = webBus("pi6",0)

def check(bus,rmList,slotList):
    for rm in rmList:
        t.openRM(bus,rm)
        for slot in slotList[4-rm]:
            uniqueID = ID(bus)
            print uniqueID.getID(slot)
            check = Checksum(uniqueID.raw)
            print check.result
            if check.result == 2:
                print 'i2c error'
            if check.result == 1:
                print 'checksum error'
            if check.result == 0:
                print 'checksum ok'

# idA = ID(bus6)
# idB = ID(bus6)
# t.openRM(bus6,2)
#
# print idA.getID(3)
# checkA = Checksum(idA.raw)
# print checkA.result
#
# print idB.getID(4)
# checkB = Checksum(idB.raw)
# print checkB.result

check(bus6,[2,1],[0,0,[3,4],[1,4]])
