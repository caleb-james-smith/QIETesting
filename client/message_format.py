#message_format.py
#Format messages.

import TestLib
t = TestLib

message = '44 33 22 11 0 0 0 100'
message = '10 11 12 13 14'
# message = '4 3 2 1'
new_message = t.reverseBytes(message)
hex_message = t.toHex(message)

print message
print new_message
print hex_message
