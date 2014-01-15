#!/usr/bin/python
# -*- coding: utf-8 -*-

#st="A55A0B06000000080001B25E002A"
#st="0"
#print(' '.join(format(x, 'b') for x in bytearray(st)))
my_hexdata = "A55A0B05000000000021CBE320FF"
scale = 16 ## equals to hexadecimalœ
num_of_bits = len(my_hexdata)*4
print(bin(int(my_hexdata, scale))[2:].zfill(num_of_bits))




#Ici on reçoit la trame 
receivedData = "A55A0B05000000000021CBE320FF"

#Ici, on traite la trame (slicing)
sep = receivedData[:4]
lenght = receivedData[4:6]
rOrg = receivedData[6:8]
data1 = receivedData[8:10]
data2 = receivedData[10:12]
data3 = receivedData[12:14]
data4 = receivedData[14:16]
ident = receivedData[16:24]
flag = receivedData[24:26]
checkSum = receivedData[26:]
print sep
print lenght
print rOrg
print data1
print data2
print data3
print data4
print ident
print flag
print checkSum
