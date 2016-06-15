from client import webBus
import TestLib as t
import QIELib as q
b = webBus("pi5",0)

def readTemp(slot, num_bytes):
    b.write(0x00,[0x06])
    b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    b.write(0x40,[0xF3])
    b.read(0x40, num_bytes)
    message = b.sendBatch()[-1]
    return getMessage(message)

def getMessage(message):
    message_list = message.split()
    message_list = message_list[1:]
    return ' '.join(message_list)

t.openRM(0)
print readTemp(0,3)
