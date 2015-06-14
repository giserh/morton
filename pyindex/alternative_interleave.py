"""
These are alternative versions of the interleave functions from interleave.py.
These were used in part to explore how the interleaving worked for 2 and 3
integers so I could use similar methods and comparisons for interleave4, and
in part to allow comparison of perfomance between the various methods.

Refs:
https://wiki.python.org/moin/BitwiseOperators
https://wiki.python.org/moin/BitManipulation
http://en.wikipedia.org/wiki/Z-order_curve
https://fgiesen.wordpress.com/2009/12/13/decoding-morton-codes/
http://www.forceflow.be/2013/10/07/morton-encodingdecoding-through-bit-interleaving-implementations/
https://graphics.stanford.edu/~seander/bithacks.html#InterleaveTableObvious
http://asgerhoedt.dk/?tag=morton-code
http://stackoverflow.com/questions/1024754/how-to-compute-a-3d-morton-number-interleave-the-bits-of-3-ints
"""

from __future__ import division

import itertools

from bitarray import bitarray
from bitstring import BitArray


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

    # convert to binary string, fill with leading zeros to 16 bit so strings
    # are same length
    x = '{:016b}'.format(x)
    y = '{:016b}'.format(y)

    # zip the two numbers (with x rightmost)
    zipped_xy = zip(y, x)
    res = ""
    for zipped_pair in zipped_xy:
        res += zipped_pair[0]
        res += zipped_pair[1]

    return int(res, base=2)


def interleave3_with_loop(x, y, z):
    """
    Reproduce the interleave2 function using for loop
    """
    # convert to binary string, fill with leading zeros to 16 bit so strings
    # are same length
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

    return int(res, base=2)


def interleave4_with_loop(v, x, y, z):
    """
    Loop method to interleave4
    """
    # convert to binary string, fill with leading zeros to 16 bit so strings
    # are same length
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

    return int(res, base=2)


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

    res = bitarray(itertools.chain.from_iterable(zip(y, x)))
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
    # convert to binary string, fill with leading zeros to 16 bit so strings
    # are same length
    x = '{:016b}'.format(x)
    y = '{:016b}'.format(y)

    # create zero filled list of length x plus length y (32)
    res = [0]*(len(x)+len(y))
    res[::2] = y
    res[1::2] = x
    res = int(''.join(res), base=2)
    return res
