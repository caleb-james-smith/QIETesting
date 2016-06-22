from client import webBus
import TestLib as t
bus5 = webBus("pi5",0)
bus6 = webBus("pi6",0)



def iglooReg(bus,rm,slot,address,nbytes):
    t.openRM(rm)
    bus.write(0x00,[0x06])
    bus.write(t.bridgeAddress(slot),[0x11,0x03,0,0,0])
    bus.write(0x09,[address])
    bus.read(0x09,nbytes)
    return bus.sendBatch()

print iglooReg(bus6,2,4,0x12,4)
