#!/usr/bin/python
# -*- coding: utf-8 -*-

my_hexdata = "85"

scale = 16 ## equals to hexadecimal

num_of_bits = 8

print bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
print bin(int("85", scale))[2:].zfill(num_of_bits)
print bin(int("0D", scale))[2:].zfill(num_of_bits)
print bin(int("0c", scale))[2:].zfill(num_of_bits)
print bin(int("0f", scale))[2:].zfill(num_of_bits)