# Read your ID for you and me!

import TestLib as t

class ID:
    def __init__(self, bus, slot):
        self.bus = bus
        self.slot = slot
        self.raw = self.getID()
        self.cooked = self.getSerial()

    def getID(self):
        # Reset entire board by writing 0x6 to 0x0.
        self.bus.write(0x00,[0x06])
        # Note that the i2c_select has register address 0x11
        # Value : 4 = 0x04 selects 0x50
        # Note that the SSN expects 32 bits (4 bytes) for writing (send 0x4, 0, 0, 0)
        self.bus.write(t.bridgeAddress(self.slot),[0x11,0x04,0,0,0])
        # Send 0x0 to 0x50 in order to set pointer for reading ID
        # This removes the permutation problem!
        self.bus.write(0x50,[0x00])
        self.bus.read(0x50,8)
        raw = self.bus.sendBatch()[-1]
        return raw

    def getSerial(self):
        if int(self.raw.split()[1]) != 0x70:
            print 'Not in Family 0x70'
            return 'Family_Code_Error'
        serial = t.serialNum(self.raw) # cereal
        oats = t.reverse(serial) # reversed
        eggs = t.toHex(oats) # hex
        return eggs
