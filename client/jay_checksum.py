#! /usr/bin/python

crctab = [
          0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65,
          157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220,
          35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98,
          190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255,
          70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7,
          219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154,
          101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36,
          248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185,
          140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205,
          17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80,
          175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238,
          50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115,
          202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139,
          87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22,
          233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168,
          116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53]

def crc(*args):
    val = 0
    args = list(args)
#    args.reverse()
    for x in args:
        val = crctab[val ^ x]
    return val

def reverse(message):
    mlist = message.split()
    error = mlist.pop(0)
    mlist.reverse()
    return error + " " + " ".join(mlist)

def toIntList(message):
    intlist = []
    mlist = message.split()
    for i in xrange(len(mlist)):
        intlist.append(int(mlist[i]))
    return intlist

def checksum(message):
    val = 0
    mlist = toIntList(message)
    error = mlist.pop(0)
    if int(error) != 0:
        print 'I2C_ERROR'
        return 2 # i2c bus error
    for x in mlist:
        val = crctab[val ^ x]
    if val != 0:
        print 'CHECKSUM_ERROR'
        return 1 # checksum error
    return True # checksum ok

idlist = [
          '0 112 138 191 234 0 0 0 132',
          '0 112 54 183 234 0 0 0 192',
          '0 112 236 157 234 0 0 0 142',
          '0 112 96 185 234 0 0 0 254',
          '0 112 121 170 215 0 0 0 212'
          ]

print crc(112, 138, 191, 234, 0, 0, 0),'\t',132
print crc(112, 54, 183, 234, 0, 0, 0),'\t',192
print crc(112, 236, 157, 234, 0, 0, 0),'\t',142
print crc(112, 96, 185, 234, 0, 0, 0),'\t',254
print crc(112, 121, 170, 215, 0, 0, 0),'\t',212

print '------------------------'

print crc(112, 138, 191, 234, 0, 0, 0, 132)
print crc(112, 54, 183, 234, 0, 0, 0, 192)
print crc(112, 236, 157, 234, 0, 0, 0, 142)
print crc(112, 96, 185, 234, 0, 0, 0, 254)
print crc(112, 121, 170, 215, 0, 0, 0, 212)

#print '------------------------'
#
#print crc(0, 0, 0, 234, 191, 138, 112),'\t',132
#print crc(0, 0, 0, 234, 183, 54, 112),'\t',192
#print crc(0, 0, 0, 234, 157, 236, 112),'\t',142
#print crc(0, 0, 0, 234, 185, 96, 112),'\t',254
#print crc(0, 0, 0, 215, 170, 121, 112),'\t',212
#
#print '------------------------'
#
#print crc(132, 0, 0, 0, 234, 191, 138, 112)
#print crc(192, 0, 0, 0, 234, 183, 54, 112)
#print crc(142, 0, 0, 0, 234, 157, 236, 112)
#print crc(254, 0, 0, 0, 234, 185, 96, 112)
#print crc(212, 0, 0, 0, 215, 170, 121, 112)

print '------------------------'

for i in xrange(len(idlist)):
    print 'ID ', i,' checksum : ', checksum(idlist[i])

