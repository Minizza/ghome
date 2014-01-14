#!/usr/bin/python
# -*- coding: utf-8 -*-

#st="A55A0B06000000080001B25E002A"
#st="0"
#print(' '.join(format(x, 'b') for x in bytearray(st)))
my_hexdata = "A55A0B05000000000021CBE320FF"
scale = 16 ## equals to hexadecimalœ
num_of_bits = len(my_hexdata)*4
print(bin(int(my_hexdata, scale))[2:].zfill(num_of_bits))

