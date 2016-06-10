#message_format.py
#Format messages.

import TestLib
t = TestLib

# message = '44 33 22 11 0 0 0 100'
message = '67 66 65'
# message = '4 3 2 1'
reversed_message = t.reverseBytes(message)
hex_message = t.toHex(reversed_message)
ascii_message = t.toASCII(reversed_message)

# print message
# print reversed_message
# print hex_message
# print ascii_message

### UniqueID Formatting Test ###
uniqueIDArray = [
    [
    '112 138 191 234 0 0 0 132',
    '112 54 183 234 0 0 0 192',
    '112 236 157 234 0 0 0 142',
    '112 96 185 234 0 0 0 254'
    ]
]

t.printIDs(uniqueIDArray)
