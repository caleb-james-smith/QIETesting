from client import webBus
from operator import add
import TestLib as t
import QIELib as q
b = webBus("pi5")

def readOnly(rm, slots):
    t.openRM(rm)
    for slot in slots:
        message = t.readRegisterBridge(slot, address, num_bytes)
