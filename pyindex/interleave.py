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

import timeit

from math import ceil


def part1by1(n):
    """
    Inserts one 0 bit between each bit in `n`.

    n: 16-bit integer
    """
    n &= 0x0000FFFF
    n = (n | (n << 8)) & 0x00FF00FF
    n = (n | (n << 4)) & 0x0F0F0F0F
    n = (n | (n << 2)) & 0x33333333
    n = (n | (n << 1)) & 0x55555555

    return n


def part1by2(n):
    """
    Inserts two 0 bits between each bit in `n`.

    n: 16-bit integer
    """
    # this is the original code from the test, so I haven't changed it, but
    # from the descriptions I've seen of the "classic" alogithms for the
    # morton code, I think the first mask should be 0x000003FF.  This would
    # mask each input number to only deal with the low 10 bits, which is the
    # maximum that can be interleaved into a 32 bit number
    n &= 0x000003FFF
    n = (n ^ (n << 16)) & 0xFF0000FF
    n = (n ^ (n << 8)) & 0x0300F00F
    n = (n ^ (n << 4)) & 0x030C30C3
    n = (n ^ (n << 2)) & 0x09249249

    return n


def part1by3(n):
    """
    Inserts three 0 bits between each bit in `n`.

    Ref: helpful description at http://stackoverflow.com/a/1024889

    n: 16-bit integer
    """
    n &= 0x000000000000FFFF
    n = (n ^ (n << 24)) & 0x000000FF000000FF
    n = (n ^ (n << 12)) & 0x000F000F000F000F
    n = (n ^ (n << 6)) & 0x0303030303030303
    n = (n ^ (n << 3)) & 0x1111111111111111
    return n


def part1by3_to_32bit(n):
    """
    Inserts three 0 bits between each bit in `n`.
    Python allows us to return 64 bits when we interleave 3 16 bits, (as in
    part1by3, but as an exercise this method assumes we're limited to 32 bits,
    so we insert three 0 bits between only the 8 low bits of n.  The only
    dfference between this and the part1by3 function is that we first mask out
    all but the lowest 8.

    n: 16-bit integer
    """
    n &= 0x000000FF
    n = (n ^ (n << 12)) & 0x000F000F
    n = (n ^ (n << 6)) & 0x03030303
    n = (n ^ (n << 3)) & 0x11111111
    return n


def unpart1by1(n):
    """
    Gets every other bit from `n`.

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
    Gets every third bit from `n`.

    n: 32-bit integer
    """
    n &= 0x09249249

    n = (n ^ (n >> 2)) & 0x030C30C3
    n = (n ^ (n >> 4)) & 0x0300F00F
    n = (n ^ (n >> 8)) & 0xFF0000FF
    n = (n ^ (n >> 16)) & 0x000003FF

    return n


def unpart1by3(n):
    """
    Gets every fourth bit from `n`.

    n: 64-bit integer
    """
    # apply mask for every fourth bit
    n &= 0x1111111111111111
    # move all bits to the right
    n = (n ^ (n >> 3)) & 0x0303030303030303
    n = (n ^ (n >> 6)) & 0x000F000F000F000F
    n = (n ^ (n >> 12)) & 0x0000FF000000FF
    n = (n ^ (n >> 24)) & 0x0000000000FFFF

    return n


def unpart1by3_from_32bit(n):
    """
    Gets every fourth bit from `n`.

    n: 32-bit integer
    """
    # apply mask for every fourth bit
    n &= 0x11111111
    # move all bits to the right
    n = (n ^ (n >> 3)) & 0x03030303
    n = (n ^ (n >> 6)) & 0x000F000F
    n = (n ^ (n >> 12)) & 0x0000FF

    return n


def interleave2(x, y):
    """
    Interleaves two integers.
    """
    max_bits = max(x.bit_length(), y.bit_length())
    # if either integer is > 16 bits, do the interleaving more than
    # once
    iterations = int(ceil(max_bits / 16))
    ret = 0
    for i in range(iterations):
        # interleave to get a 32 bit integer
        interleaved = part1by1(x & 0xFFFF) | \
                      (part1by1(y & 0xFFFF) << 1)
        # left shift the interleaved numbers for this iteration
        ret |= (interleaved << (32 * i))
        # right shift x and y by 16 so we do the next iteration on the
        # next 16 digits
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


def interleave4(v, x, y, z):
    """
    Interleaves four integers and returns a 64 bit integer.
    """
    return (
        part1by3(v) | (part1by3(x) << 1) |
        (part1by3(y) << 2) | (part1by3(z) << 3)
        )


def interleave4_to_32bit(v, x, y, z):
    """
    Interleaves four integers and returns a 32 bit integer.

    Python allows us to return 64 bits when we interleave 3 16 bits, (as in
    inteleave4), but as an exercise this method assumes we're limited to 32
    bits.
    """
    return (
        part1by3_to_32bit(v) | (part1by3_to_32bit(x) << 1) |
        (part1by3_to_32bit(y) << 2) | (part1by3_to_32bit(z) << 3)
        )


def interleave4_any_length_input(v, x, y, z):
    """
    Allow interleaving of 4 integers of any (equal) length by finding the
    maximum length of each of them and iterating over groups of 16-bit integer
    to build up the interleaved number

    Note that if the integers are different bit lengths, the shorter integer is
    still zero padded (this is also the case for interleave2).
    """

    max_bits = max(
        v.bit_length(), x.bit_length(), y.bit_length(), z.bit_length()
    )
    # if any integer is > 16 bits, do the interleaving more than
    # once
    iterations = int(ceil(max_bits / 16))
    ret = 0
    for i in range(iterations):
        # interleave to get a 64 bit integer
        interleaved = part1by3(v & 0xFFFF) | \
                      (part1by3(x & 0xFFFF) << 1) | \
                      (part1by3(y & 0xFFFF) << 2) | \
                      (part1by3(z & 0xFFFF) << 3)
        # left shift the interleaved numbers for this iteration
        ret |= (interleaved << (64 * i))
        # right shift v, x, y and z by 16 so we do the next iteration on the
        # next 16 digits
        v >>= 16
        x >>= 16
        y >>= 16
        z >>= 16
    return ret


def deinterleave4(n):
    """
    Deinterleaves a 64-bit integer into four 16-bit integers.
    """
    return (
        unpart1by3(n),
        unpart1by3(n >> 1),
        unpart1by3(n >> 2),
        unpart1by3(n >> 3)
        )


def deinterleave4_from_32bit(n):
    """
    Deinterleaves a 32-bit integer into four 16-bit integers.
    """
    return (
        unpart1by3_from_32bit(n),
        unpart1by3_from_32bit(n >> 1),
        unpart1by3_from_32bit(n >> 2),
        unpart1by3_from_32bit(n >> 3)
        )


def deinterleave4_any_length_input(n):
    """
    Deinterleaves an integer of any length into 4 integers
    """
    # find the number of iterations of deinterleaving 4 16 bit integers
    # (64 total) we need to do
    iterations = int(ceil(n.bit_length() / 64))

    v = x = y = z = 0
    for i in range(iterations):
        # unpart each 64-bit chunk into 4 16-bit integers, then left shift each
        # 16-bit chunk of each deinterleaved number by 16 to leave room at the
        # right for the next chunk
        v |= unpart1by3(n) << (16 * i)
        x |= unpart1by3(n >> 1) << (16 * i)
        y |= unpart1by3(n >> 2) << (16 * i)
        z |= unpart1by3(n >> 3) << (16 * i)
        # right shift the original number by 64 so the next iteration deals
        # with the next chunk of 64 bits
        n = n >> 64

    return v, x, y, z


def make_mask(masklength, oneslength, zeroslength):
    """
    Create a mask of repeating groups of ones and zeros of total length
    given by masklength. Each mask group starts with ones.

    masklength: bitlength of final mask
    oneslength: number of ones in each mask group
    zeroslength: number of zeros in each mask group

    """
    # number of groups of ones and zeros in the total mask length
    mask_groups = masklength // (oneslength + zeroslength)

    # start with the number of ones in the first mask group
    # eg. mask to be 00110011
    first_ones = 1
    for i in xrange(oneslength - 1):
        first_ones = (first_ones << 1) | first_ones
    # first_ones = 11

    # left shift by the number of zeros
    mask = first_ones << zeroslength
    # mask = 1100
    # this makes one mask group after the initial ones

    for i in xrange(mask_groups - 1):
        # << by length of ones + zeros, | by itself
        mask = mask << (oneslength + zeroslength) | mask
        # mask = 11001100

    # add in the first ones:
    # shift by the number of ones in the first group, | with first_ones
    mask = (mask << oneslength) | first_ones

    # remove the extra leading ones group
    onesmask = 1
    for i in xrange(masklength - 1):
        onesmask = (onesmask << 1) | onesmask

    return mask & onesmask


def part1by(n, offset):
    """
    Insert the number of 0 bits given by 'offset' between each bit in n

    n: 16 bit integer

    """
    # mask the input n to the appropriate number of bits that can be
    # interleaved in 32bit
    bits_to_include = 32 // (offset + 1)
    mask = 1
    for i in xrange(bits_to_include - 1):
        mask = (mask << 1) | mask
    n &= mask

    # split 16bit into two 8bit groups with enough zero bits inbetween
    # to fit the other numbers when interleaved, by shifting by offset * 8
    n = (n ^ (n << (offset * 8))) & make_mask(32, 8, offset * 8)
    # split to 4 4bit groups
    n = (n ^ (n << (offset * 4))) & make_mask(32, 4, offset * 4)
    # split to 8 2bit groups
    n = (n ^ (n << (offset * 2))) & make_mask(32, 2, offset * 2)
    # split to 16 single bit groups
    n = (n ^ (n << offset)) & make_mask(32, 1, offset)

    return n


def part1byany(n, offset):
    """
    Insert the number of 0 bits given by 'offset' between each bit in n

    n: 16 bit integer

    """
    # mask the input n to 16
    n &= 0xFFFF
    # split 16bit into two 8bit groups with enough zero bits inbetween
    # to fit the other numbers when interleaved, by shifting by offset * 8
    n = (n ^ (n << (offset * 8))) & make_mask(16 * (offset + 1), 8, offset * 8)
    # split to 4 4bit groups
    n = (n ^ (n << (offset * 4))) & make_mask(16 * (offset + 1), 4, offset * 4)
    # split to 8 2bit groups
    n = (n ^ (n << (offset * 2))) & make_mask(16 * (offset + 1), 2, offset * 2)
    # split to 16 single bit groups
    n = (n ^ (n << offset)) & make_mask(16 * (offset + 1), 1, offset)

    return n


def interleave_any(*integers):
    """
    Interleave any number of integers to a 32 bit integer
    Although we can give this function any number of integers, if we try to
    interleave too many, the output is unlikely to be useful because too much
    information will be lost (e.g. with 10 numbers, only 3 of each are used
    when interleaved to a single 32 bit integer).

    This could be extended by using a similar method to interleave2, to
    calculate the maximum bit length of the input numbers and repeat the
    interleaving for each 16 bit section

    integers: 16 bit integers
    """
    # number of integers to interleave
    count = len(integers)
    # part each integer by count - 1
    parted_integers = [part1by(integer, count - 1) for integer in integers]
    # shift the parted integers for inteleaving
    shifted = [integer << i for i, integer in enumerate(parted_integers)]
    # interleave the parted integers
    res = shifted[0]
    for shifted_num in shifted[1:]:
        res |= shifted_num
    return res


def interleave_any_16bit_to_any_length_output(*integers):
    """
    Interleave any number of integers

    This only interleaves input numbers of max 16 bits, but could be extended
    by using a similar method to interleave2 and interleave4_any_length_input,
    to calculate the maximum bit length of the input numbers and repeat the
    interleaving for each 16 bit section

    integers: 16 bit integers
    """
    # number of integers to interleave
    count = len(integers)
    # part each integer by count - 1
    parted_integers = [part1byany(integer, count - 1) for integer in integers]
    # shift the parted integers for inteleaving
    shifted = [integer << i for i, integer in enumerate(parted_integers)]
    # interleave the parted integers
    res = shifted[0]
    for shifted_num in shifted[1:]:
        res |= shifted_num
    return res


INCLUDE_MASK_TABLE = [
    0x0000FFFF, 0x000003FF, 0x000000FF, 0x0000003F, 0x0000001F, 0x0000000F,
    0x0000000F, 0x00000007, 0x00000003
]

MASK_TABLE = [
    [0x00FF00FF, 0xF0F0F0F, 0x33333333, 0x55555555],
    [0xFF0000FF, 0xF00F00F, 0xC30C30C3, 0x49249249],
    [0x000000FF, 0x000F000F, 0x03030303, 0X11111111],
    [0x000000FF, 0x00F0000F, 0xC0300C03, 0x42108421],
    [0x000000FF, 0x00F0000F, 0xC0300C03, 0x41041041],
    [0x000000FF, 0xF000000F, 0x3000C003, 0x10204081],
    [0x000000FF, 0xF000000F, 0x3000C003, 0x01010101],
    [0x000000FF, 0x0000000F, 0x000C0003, 0x08040201],
    [0x000000FF, 0x0000000F, 0x00300003, 0X40100401]
]


def part1by_with_lookup(n, offset):
    """
    Insert the number of 0 bits given by 'offset' between each bit in n
    Use a table of masks to improve perfromance.  The
    table includes masks for interleaving up to 10 integers.

    n: 16 bit integer.
    """
    bits_to_include = INCLUDE_MASK_TABLE[offset - 1]
    n = (n ^ (n << (offset * 8))) & MASK_TABLE[offset - 1][0]
    n = (n ^ (n << (offset * 4))) & MASK_TABLE[offset - 1][1]
    n = (n ^ (n << (offset * 2))) & MASK_TABLE[offset - 1][2]
    n = (n ^ (n << offset)) & MASK_TABLE[offset - 1][3]

    return n


def interleave_any_with_lookup_table(*integers):
    """
    Interleave any given integers to 32 bit number using lookup tables for
    efficiency.   The table includes masks for interleaving up to 10 integers.

    integers: 16 bit integers
    """
    # number of integers to interleave
    count = len(integers)
    # part each integer by count - 1
    parted_integers = [
        part1by_with_lookup(integer, count - 1) for integer in integers
    ]
    # shift the parted integers for inteleaving
    shifted = [integer << i for i, integer in enumerate(parted_integers)]
    # interleave the parted integers
    res = shifted[0]
    for shifted_num in shifted[1:]:
        res |= shifted_num
    return res


def interleave_any_input_output(*integers):
    """
    Interleave any number of integers of any (equal) length

    Note that if the integers are different bit lengths, the shorter integer is
    still zero padded (this is also the case for interleave2).

    integers: integers of any length
    """
    max_bits = max([integer.bit_length() for integer in integers])

    # if any integer is > 16 bits, do the interleaving more than
    # once
    iterations = int(ceil(max_bits / 16))
    ret = 0

    # number of integers to interleave
    count = len(integers)
    ret = 0
    for i in range(iterations):
        # part each 16-bit chunk of the integer by count - 1
        parted_integers = [part1byany(integer, count - 1) for integer in integers]
        # shift the parted integers for interleaving
        shifted = [integer << j for j, integer in enumerate(parted_integers)]
        # interleave the parted integers
        interleaved = shifted[0]
        for shifted_num in shifted[1:]:
            interleaved |= shifted_num
        # left shift the interleaved integers for this iteration
        interleaved = interleaved << (16 * count * i)
        # add this chunk of interleaved integers to the result
        ret |= interleaved
        # right shift each of the input integers by 16 so we do the next
        # iteration on the next 16 digits
        integers = [integer >> 16 for integer in integers]

    return ret


def time_taken(*args, **kwargs):
    """
    A function to time the various interleave functions.  Take the minimum of
    1000 runs to reduce measurement distortions due to other processes.

    args: functions to test
    kwargs['integers']: a tuple of integers to be passed to the function

    INTERLEAVE2 Results
    -------------------
    time_taken(interleave2, interleave2_with_loop, interleave2_with_bitarray,
        interleave2_with_bitarray_and_chain,
            interleave2_with_bitstring_and_chain, interleave2_with_slicing,
            interleave_any, interleave_any_16bit_to_any_length_output,
            interleave_any_input_output, interleave_any_with_lookup_table,
            interleave_32, integers=(0xFFFF, 0x0000))
    Function (interleave.interleave2): 4.577637e-05
    Function (alternative_interleave.interleave2_with_loop): 9.393692e-05
    Function (alternative_interleave.interleave2_with_bitarray): 1.239777e-04
    Function (alternative_interleave.interleave2_with_bitarray_and_chain):
        9.489059e-05
    Function (alternative_interleave.interleave2_with_bitstring_and_chain):
        6.208420e-04
    Function (alternative_interleave.interleave2_with_slicing): 8.392334e-05
    Function (interleave.interleave_any): 6.270409e-04
    Function (interleave.interleave_any_16bit_to_any_length_output):
        6.270409e-04
    Function (interleave.interleave_any_input_output): 6.179810e-04
    Function (interleave.interleave_any_with_lookup_table): 5.388260e-05

    Comparison with lookup table method from morton.py:
    Function (morton.interleave_32): 1.597404e-05

    INTERLEAVE3 Results
    -------------------
    time_taken(interleave3, interleave3_with_loop, interleave_any,
        interleave_any_16bit_to_any_length_output, interleave_any_input_output,
        interleave_any_with_lookup_table, integers=(0xFFFF, 0x0000, 0xFFFF))
    Function (interleave.interleave3): 3.194809e-05
    Function (alternative_interleave.interleave3_with_loop): 1.199245e-04
    Function (interleave.interleave_any): 8.487701e-04
    Function (interleave.interleave_any_16bit_to_any_length_output): 1.087904e-03
    Function (interleave.interleave_any_input_output): 1.122952e-03
    Function (interleave.interleave_any_with_lookup_table): 7.581711e-05

    INTERLEAVE4 Results
    -------------------
    time_taken(interleave4, interleave4_to_32bit, interleave4_any_length_input,
        interleave_any, interleave_any_16bit_to_any_length_output,
        interleave_any_input_output, interleave_any_with_lookup_table,
        integers=(0xFFFF, 0x0000, 0xFFFF, 0x0000))
    Function (interleave.interleave4): 3.886223e-05
    Function (interleave.interleave4_to_32bit): 3.290176e-05
    Function (interleave.interleave4_any_length_input): 6.389618e-05
    Function (interleave.interleave_any): 1.093864e-03
    Function (interleave.interleave_any_16bit_to_any_length_output): 1.870871e-03
    Function (interleave.interleave_any_input_output): 1.908064e-03
    Function (interleave.interleave_any_with_lookup_table): 8.797646e-05

    """
    for func in args:
        min_time = min(
            timeit.Timer(
                lambda: func(*kwargs['integers']), setup=''
            ).repeat(1000, 10)
        )
        print(
            "Function ({}.{}): {:e}".format(
                func.__module__, func.__name__, min_time
            )
        )
