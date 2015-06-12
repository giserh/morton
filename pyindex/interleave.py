# -*- coding: utf-8 -*-

"""
This is the equivalent of what you find in morton.py except that these
functions do not use lookup tables to do the work and that you can
(de)interleave 3 integers together.

In theory, these functions could work regardless of the size of the
integers you pass in. This should come later, altough you should expect
them to be slower.
"""
from __future__ import division

import itertools
import timeit

from bitarray import bitarray
from bitstring import BitArray

from math import ceil


def part1by1(num):
    """
    Inserts one 0 bit between each bit in `num`.

    num: 16-bit integer
    """
    num &= 0x0000FFFF

    num = (num | (num << 8)) & 0x00FF00FF
    num = (num | (num << 4)) & 0x0F0F0F0F
    num = (num | (num << 2)) & 0x33333333
    num = (num | (num << 1)) & 0x55555555

    return num


def part1by2(num):
    """
    Inserts two 0 bits between each bit in `num`.

    num: 16-bit integer
    """
    num &= 0x000003FF # seemed to be an extra F here?
    num = (num ^ (num << 16)) & 0xFF0000FF
    num = (num ^ (num << 8)) & 0x0300F00F
    num = (num ^ (num << 4)) & 0x030C30C3
    num = (num ^ (num << 2)) & 0x09249249

    return num

def part1by3(num):
    """
    Inserts three 0 bits between each bit in `num`.

    helpful description: http://stackoverflow.com/a/1024889

    num: 16-bit integer
    """
    num &= 0x00000000FFFF
    num = (num ^ (num << 16)) & 0x00FF00FF00FF
    num = (num ^ (num << 8)) & 0x0F0F0F0F0F0F
    num = (num ^ (num << 4)) & 0x0C30C30C30C3
    import ipdb; ipdb.set_trace()

    num = (num ^ (num << 3)) & 0x111111111111
    import ipdb; ipdb.set_trace()
    pass

def unpart1by1(n):
    """
    Gets every other bits from `n`.

    n: 32-bit integer
    """
    n &= 0x55555555

    n = (n ^ (n >> 1)) & 0x33333333
    n = (n ^ (n >> 2)) & 0x0F0F0F0F
    n = (n ^ (n >> 4)) & 0x00FF00FF
    n = (n ^ (n >> 8)) & 0x0000FFFF

    return n


def unpart1by2(n):
    """
    Gets every third bits from `n`.

    n: 32-bit integer
    """
    n &= 0x09249249

    n = (n ^ (n >> 2)) & 0x030C30C3
    n = (n ^ (n >> 4)) & 0x0300F00F
    n = (n ^ (n >> 8)) & 0xFF0000FF
    n = (n ^ (n >> 16)) & 0x000003FF

    return n


def interleave2(x, y):
    """
    Interleaves two integers.
    """
    max_bits = max(x.bit_length(), y.bit_length())
    iterations = int(ceil(max_bits / 16))
    ret = 0
    for i in range(iterations):
        interleaved = part1by1(x & 0xFFFF) | \
                      (part1by1(y & 0xFFFF) << 1)
        ret |= (interleaved << (32 * i))

        x = x >> 16
        y = y >> 16
    return ret


def deinterleave2(n):
    """
    Deinterleaves an integer into two integers.
    """
    iterations = int(ceil(n.bit_length() / 32))

    x = y = 0
    for i in range(iterations):
        x |= unpart1by1(n) << (16 * i)
        y |= unpart1by1(n >> 1) << (16 * i)
        n = n >> 32

    return x, y


def interleave3(x, y, z):
    """
    Interleaves three integers.
    """
    return part1by2(x) | (part1by2(y) << 1) | (part1by2(z) << 2)


def deinterleave3(n):
    """
    Deinterleaves an integer into three integers.
    """
    return unpart1by2(n), unpart1by2(n >> 1), unpart1by2(n >> 2)


def interleave2_with_loop(x, y):
    """
    Reproduce the interleave2 function using a loop
    """
    # # convert to binary, strip leading "0b" (initial method used)
    # x = str(bin(x))[2:]
    # y = str(bin(y))[2:]
    # # fill with leading zeros to 16 bit
    # x = x.zfill(16)
    # y = y.zfill(16)

    # # convert to binary, fill with leading zeros to 16 bit
    x = '{:016b}'.format(x)
    y = '{:016b}'.format(y)

    # zip the two numbers (with x rightmost)
    zipped_xy = zip(y, x)
    res = ""
    for zipped_pair in zipped_xy:
        res += zipped_pair[0]
        res += zipped_pair[1]

    return int(res, base = 2)

def interleave3_with_loop(x, y, z):
    """
    Reproduce the interleave2 function using for loop
    """
    # # convert to binary, fill with leading zeros to 16 bit
    x = '{:016b}'.format(x)
    y = '{:016b}'.format(y)
    z = '{:016b}'.format(z)

    # zip the 3 numbers (with x rightmost)
    zipped_xyz = zip(z, y, x)
    res = ""
    for zipped_pair in zipped_xyz:
        res += zipped_pair[0]
        res += zipped_pair[1]
        res += zipped_pair[2]

    return int(res, base = 2)


def interleave4_with_loop(v, x, y, z):
    """
    Loop method to interleave4
    """
    # # convert to binary, fill with leading zeros to 16 bit
    v = '{:016b}'.format(v)
    x = '{:016b}'.format(x)
    y = '{:016b}'.format(y)
    z = '{:016b}'.format(z)

    # zip the 4 numbers (with v rightmost)
    zipped_vxyz = zip(z, y, x, v)
    res = ""
    for zipped_pair in zipped_vxyz:
        res += zipped_pair[0]
        res += zipped_pair[1]
        res += zipped_pair[2]
        res += zipped_pair[3]

    return int(res, base = 2)


def interleave2_with_bitarray(x, y):
    """
    Reproduce the interleave2 function using bitarray module
    """
    x = bitarray('{:016b}'.format(x))
    y = bitarray('{:016b}'.format(y))

    zipped = zip(y, x)
    # http://stackoverflow.com/a/3472379
    res = bitarray([item for zipped_pair in zipped for item in zipped_pair])
    return int(res.to01(), base=2)


def interleave2_with_bitarray_and_chain(x, y):
    """
    Reproduce the interleave2 function using bitarray module and itertools
    chain
    """
    x = bitarray('{:016b}'.format(x))
    y = bitarray('{:016b}'.format(y))

    res = bitarray(itertools.chain.from_iterable(zip(y,x)))
    return int(res.to01(), base=2)


def interleave2_with_bitstring_and_chain(x, y):
    """
    Reproduce the interleave2 function using bitstring module and itertools
    chain
    """
    x = BitArray(bin(x)).bin.zfill(16)
    y = BitArray(bin(y)).bin.zfill(16)
    zipped_xy = zip(y, x)
    res = ""
    for zipped_pair in zipped_xy:
        res += zipped_pair[0]
        res += zipped_pair[1]
    return int(res, base=2)


def interleave2_with_slicing(x, y):
    """
    Reproduce the interleave2 using string splicing
    http://stackoverflow.com/a/26013222
    """
    # convert to binary, fill with leading zeros to 16 bit so strings are same
    # length
    x = '{:016b}'.format(x)
    y = '{:016b}'.format(y)

    # create zero filled list of length x plus length y (32)
    res = [0]*(len(x)+len(y))
    res[::2] = y
    res[1::2] = x
    res = int(''.join(res), base=2)
    return res



def time_taken(func, integers):
    """
    A function to time the various interleave functions.  Take the minimum of
    50 runs to reduce measurement distortions due to other processes.

    func: an interleave function
    integers: a tuple of integers to be passed to the function

    INTERLEAVE2 Results
    -------------------
    time_taken(func, (4, 42))
    Function (interleave2): 4.261017e-03
    Function (interleave2_with_loop): 8.367062e-03
    Function (interleave2_with_bitarray): 1.183796e-02
    Function (interleave2_with_bitarray_and_chain): 8.599997e-03
    Function (interleave2_with_bitstring_and_chain): 5.829000e-02
    Function (interleave2_with_slicing): 8.026123e-03

    INTERLEAVE3 Results
    -------------------
    time_taken(func, (4, 42, 54))
    Function (interleave3): 3.561974e-03
    Function (interleave3_with_loop): 1.097608e-02

    """
    min_time = min(
        timeit.Timer(lambda: func(*integers), setup='').repeat(50, 1000)
    )
    print("Function ({}): {:e}".format(func.__name__, min_time))
