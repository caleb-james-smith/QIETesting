from client import webBus
import caleb_checksum as cc
import TestLib as t
import QIELib as q
bus = webBus("pi5")

def readTemp(slot, num_bytes):
    bus.write(0x00,[0x06])
    bus.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    bus.write(0x40,[0xF3])
    bus.read(0x40, num_bytes + 2)
    message = bus.sendBatch()[-1]
    message_list = message.split()
    a = message_list[1]
    b = message_list[2]
    checksum = message_list[3]
    return getMessage(message)

def getMessage(message):
    message_list = message.split()
    message_list = message_list[1:]
    return ' '.join(message_list)

def calcTemp(s):
    return -46.85 + 175.72 * s/2**16

def calcHumi(s):
    return -6 + 125.0 * s/2**16

t.openRM(0)
print readTemp(0,2)

# Set last two bits of LSB to 0 (these are status bits).
# message = '0 01100011 01010010 01100100'
# 0110'0011'0101'0000 = 25424.


# Trigger T measurement     hold master     1110'0011   0xE3
# Trigger RH measurement    hold master     1110'0101   0xE5
# Trigger T measurement     no hold master  1111'0011   0xF3
# Trigger RH measurement    no hold master  1111'0101   0xF5
