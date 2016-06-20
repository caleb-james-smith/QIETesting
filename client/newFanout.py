# new fanout pi6

from client import webBus
import TestLib as t
from caleb_checksum import checkCRC
b = webBus("pi6",1)

def ngccmGroup(rm):
    i2cGroups = [0x01,0x10,0x20,0x02]
    return i2cGroups[rm-1]

def open(rm):
    if rm in [0,1]:
        # Open channel to ngCCM for RM 0,1: J1 - J10
        print '### Open RM ', rm
        b.write(0x72,[0x02])
        # b.sendBatch()
    elif rm in [2,3]:
        # Open channel to ngCCM for RM 2,3: J17 - J26
        print '### Open RM ', rm
        b.write(0x72,[0x01])
        # b.sendBatch()
    else:
        print 'Invalid RM = ', rm
        print 'Please choose RM = {0,1,2,3}'
        return 'closed channel'
    # Open channel to i2c group
    # print '##### open i2c ' + hex(q.RMi2c[rm])
    # b.clearBus()
    b.write(0x74, [ngccmGroup(rm)])
    return b.sendBatch()

print open(0)
