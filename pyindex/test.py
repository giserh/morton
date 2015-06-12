#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Some tests for pyindex (currently just very basic tests for interleave.py)"""

import unittest
import interleave

class TestInterleave(unittest.TestCase):

    def test_interleave2(self):
        self.assertEqual(hex(interleave.interleave2(0x00, 0xFF)), '0xaaaa')
        self.assertEqual(hex(interleave.interleave2(0x0000, 0xFFFF)), '0xaaaaaaaa')

    def test_interleave3(self):
        self.assertEqual(hex(interleave.interleave3(0x00, 0xFF, 0x00)), '0x492492')
        self.assertEqual(hex(interleave.interleave3(0x0000, 0xFFFF, 0x0000)), '0x12492492')

    def test_idempotency(self):
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        self.assertEqual(integers, interleave.deinterleave2(interleaved))

    def test_interleave2_with_loop(self):
        """
        test that loop version of interleave2 produces the same results as
        the original
        """
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        interleaved_with_loop = interleave.interleave2_with_loop(*integers)
        self.assertEqual(interleaved, interleaved_with_loop)

    def test_interleave3_with_loop(self):
        """
        test that loop version of interleave3 produces the same results as
        the original
        """
        integers = (4, 42, 7)
        interleaved = interleave.interleave3(*integers)
        interleaved_with_loop = interleave.interleave3_with_loop(*integers)
        self.assertEqual(interleaved, interleaved_with_loop)

    def test_interleave4_with_loop(self):
        integers = (3, 9, 7, 8)
        self.assertEqual(
            hex(interleave.interleave4_with_loop(*integers)), '0xa457'
        )

    def test_interleave2_with_bitarray(self):
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        interleaved_with_bitarray = interleave.interleave2_with_bitarray(
            *integers
        )
        self.assertEqual(interleaved, interleaved_with_bitarray)

    def test_interleave2_with_bitarray_and_chain(self):
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        interleaved_with_bitarray = \
            interleave.interleave2_with_bitarray_and_chain(*integers)
        self.assertEqual(interleaved, interleaved_with_bitarray)

    def test_interleave2_with_bitstring_and_chain(self):
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        interleaved_with_bitstring = \
            interleave.interleave2_with_bitstring_and_chain(*integers)
        self.assertEqual(interleaved, interleaved_with_bitstring)

    def test_interleave2_with_slicing(self):
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        interleave_with_slicing = \
            interleave.interleave2_with_slicing(*integers)
        self.assertEqual(interleaved, interleave_with_slicing)


if __name__ == '__main__':
    unittest.main()
