# Format

# Split message into a list of messages. Use for QIE Dasiy Chains.
def splitMessage(message, num_parts):
    message_list = message.split()
    size = len(message_list) / num_parts
    final_message_list = []
    s = " "
    for n in xrange(num_parts):
        part_list = message_list[n*size:(n+1)*size]
        final_message_list.append(s.join(part_list))
    return final_message_list


def reverse(message):
    mList = message.split()
    mList.reverse()
    s = " "
    return s.join(mList)

# Reverse order of string of bytes separated by spaces.
# Leaves errorCode as first (leftmost) byte
def reverseBytes(message):
    mList = message.split()
    errorCode = mList.pop(0)
    mList.reverse()
    finalList = [errorCode] + mList
    s = " "
    return s.join(finalList)

# reverse all bits
def reverseBits(message):
    mList = message.split()
    errorCode = mList.pop(0)
    for n in xrange(len(mList)):
        bits = bin(int(mList[n]))[2:]
        reversedBits = bits[::-1]
        mList[n] = str(int(reversedBits,2))
    finalList = [errorCode] + mList
    s = " "
    return s.join(finalList)

def reverseKeepCRC(message):
    mList = message.split()
    errorCode = mList.pop(0)
    checksum = mList.pop()
    mList.reverse()
    finalList = [errorCode] + mList + [checksum]
    s = " "
    return s.join(finalList)

# Use ony 6 byte serial number
def serialNumCRC(message):
    mList = message.split()
    errorCode = mList.pop(0)
    mList.pop(0)
    finalList = [errorCode] + mList
    s = " "
    return s.join(finalList)

# Reverse order of string of bytes separated by spaces.
# Leaves errorCode as first (leftmost) byte.
# Leaves checksum as last (rightmost) byte.
def reverseSerial(message):
    mList = message.split()
    errorCode = mList.pop(0)
    familyCode = mList.pop(0)
    checksum = mList.pop()
    mList.reverse()
    finalList = [errorCode] + [familyCode] + mList + [checksum]
    s = " "
    return s.join(finalList)

def moveFamilyCode(message):
    mList = message.split()
    errorCode = mList.pop(0)
    familyCode = mList.pop(0)
    checksum = mList.pop()
    finalList = [errorCode] + mList + [familyCode] + [checksum]
    s = " "
    return s.join(finalList)

# Convert string of ints to list of ints.
def toIntList(message):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = int(message_list[byte])
    return message_list

# Convert string of ints with spaces to a string of hex values with no spaces... one long string.
def toHex(message, colon=2):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = hex(int(message_list[byte]))
        message_list[byte] = message_list[byte][2:]
        if len(message_list[byte]) == 1:
            message_list[byte] = '0' + message_list[byte]
    if colon == 2:
        s = ":"
        return s.join(message_list)
    if colon == 1:
        s = " "
        return s.join(message_list)
    s = ""
    return '0x' + s.join(message_list)

# Parse Serial Number (6 bytes) from 8 byte Registration Number.
def serialNum(message):
    message_list = message.split()
    message_list = message_list[2:-1]
    s = " "
    return s.join(message_list)

#ASCII
def toASCII(message):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = chr(int(message_list[byte]))
    s = ""
    return s.join(message_list)
