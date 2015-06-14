#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Some tests for pyindex (currently just very basic tests for interleave.py)
"""

import unittest
import interleave
import alternative_interleave


class TestInterleave(unittest.TestCase):

    def test_interleave2(self):
        self.assertEqual(
            hex(interleave.interleave2(0x00, 0xFF)), '0xaaaa'
        )
        self.assertEqual(
            hex(interleave.interleave2(0x0000, 0xFFFF)), '0xaaaaaaaa'
        )

    def test_interleave2_with_integers_longer_than_16bit(self):
        # interleave2 can interleave integers larger than 16bits
        self.assertEqual(
            hex(interleave.interleave2(0xFFFFFFFF, 0xFFFFFFFF)),
            '0xffffffffffffffffL'
        )
        # but if the integers are different lengths it doesn't flatten them
        self.assertNotEqual(
            hex(interleave.interleave2(0xF, 0xFF)),
            '0xfff'
        )
        self.assertEqual(
            hex(interleave.interleave2(0xF, 0xFF)),
            '0xaaff'
        )

    def test_interleave3(self):
        self.assertEqual(
            hex(interleave.interleave3(0x00, 0xFF, 0x00)), '0x492492'
        )
        self.assertEqual(
            hex(interleave.interleave3(0x0000, 0xFFFF, 0x0000)), '0x12492492'
        )

    def test_interleave4(self):
        self.assertEqual(
            hex(interleave.interleave4(0xF, 0x0, 0xF, 0x0)), '0x5555'
        )
        self.assertEqual(
            hex(interleave.interleave4(0xFF, 0x00, 0xFF, 0x00)), '0x55555555'
        )
        self.assertEqual(
            hex(
                interleave.interleave4(0xFFFF, 0x0000, 0xFFFF, 0x0000)
            ), '0x5555555555555555'
        )
        integers = (3, 9, 7, 8)
        self.assertEqual(
            hex(interleave.interleave4_to_32bit(*integers)), '0xa457'
        )

    def test_interleave4_to_32bit(self):
        self.assertEqual(
            hex(interleave.interleave4_to_32bit(0xF, 0x0, 0xF, 0x0)), '0x5555'
        )
        self.assertEqual(
            hex(
                interleave.interleave4_to_32bit(0xFF, 0x00, 0xFF, 0x00)
            ), '0x55555555'
        )
        self.assertEqual(
            hex(
                interleave.interleave4_to_32bit(0xFFFF, 0x0000, 0xFFFF, 0x0000)
            ), '0x55555555'
        )

        integers = (3, 9, 7, 8)
        self.assertEqual(
            hex(interleave.interleave4_to_32bit(*integers)), '0xa457'
        )

    def test_idempotency(self):
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        self.assertEqual(integers, interleave.deinterleave2(interleaved))

    def test_interleave2_with_loop_comparison(self):
        """
        test that loop version of interleave2 produces the same results as
        the original
        """
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        interleaved_with_loop = alternative_interleave.interleave2_with_loop(
            *integers
        )
        self.assertEqual(interleaved, interleaved_with_loop)

    def test_interleave3_with_loop_comparison(self):
        """
        test that loop version of interleave3 produces the same results as
        the original
        """
        integers = (4, 42, 7)
        interleaved = interleave.interleave3(*integers)
        interleaved_with_loop = alternative_interleave.interleave3_with_loop(
            *integers
        )
        self.assertEqual(interleaved, interleaved_with_loop)

    def test_interleave4_with_loop(self):
        integers = (3, 9, 7, 8)
        self.assertEqual(
            hex(
                alternative_interleave.interleave4_with_loop(*integers)
            ),
            '0xa457'
        )

    def test_interleave2_with_bitarray(self):
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        interleaved_with_bitarray = alternative_interleave.\
            interleave2_with_bitarray(*integers)
        self.assertEqual(interleaved, interleaved_with_bitarray)

    def test_interleave2_with_bitarray_and_chain(self):
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        interleaved_with_bitarray = alternative_interleave.\
            interleave2_with_bitarray_and_chain(*integers)
        self.assertEqual(interleaved, interleaved_with_bitarray)

    def test_interleave2_with_bitstring_and_chain(self):
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        interleaved_with_bitstring = alternative_interleave.\
            interleave2_with_bitstring_and_chain(*integers)
        self.assertEqual(interleaved, interleaved_with_bitstring)

    def test_interleave2_with_slicing(self):
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        interleave_with_slicing = alternative_interleave\
            .interleave2_with_slicing(*integers)
        self.assertEqual(interleaved, interleave_with_slicing)

    def test_idempotency_3(self):
        integers = (4, 42, 36)
        interleaved = interleave.interleave3(*integers)
        self.assertEqual(integers, interleave.deinterleave3(interleaved))

    def test_idempotency_4(self):
        integers = (4, 42, 36, 78)
        interleaved = interleave.interleave4(*integers)
        self.assertEqual(integers, interleave.deinterleave4(interleaved))

        interleaved = interleave.interleave4_to_32bit(*integers)
        self.assertEqual(
            integers, interleave.deinterleave4_from_32bit(interleaved)
        )

    def test_interleave_any_with_2_integers(self):
        self.assertEqual(
            hex(interleave.interleave_any(0x00, 0xFF)), '0xaaaa'
        )
        self.assertEqual(
            hex(interleave.interleave_any(0x0000, 0xFFFF)), '0xaaaaaaaa'
        )

    def test_interleave_any_with_3_integers(self):
        self.assertEqual(
            hex(interleave.interleave_any(0x00, 0xFF, 0x00)), '0x492492'
        )
        self.assertEqual(
            hex(interleave.interleave_any(0x0000, 0xFFFF, 0x0000)),
            '0x12492492'
        )

    def test_interleave_any_with_4_integers(self):
        self.assertEqual(
            hex(interleave.interleave_any(0xF, 0x0, 0xF, 0x0)), '0x5555'
        )
        self.assertEqual(
            hex(
                interleave.interleave_any(0xFF, 0x00, 0xFF, 0x00)
            ), '0x55555555'
        )
        self.assertEqual(
            hex(
                interleave.interleave_any(0xFFFF, 0x0000, 0xFFFF, 0x0000)
            ), '0x55555555'
        )

        integers = (3, 9, 7, 8)
        self.assertEqual(
            hex(interleave.interleave_any(*integers)), '0xa457'
        )

    def test_interleave_any_with_4_integers_with_lookup(self):
        self.assertEqual(
            hex(
                interleave.interleave_any_with_lookup_table(
                    0xF, 0x0, 0xF, 0x0
                )
            ), '0x5555'
        )
        self.assertEqual(
            hex(
                interleave.interleave_any_with_lookup_table(
                    0xFF, 0x00, 0xFF, 0x00
                )
            ), '0x55555555'
        )
        self.assertEqual(
            hex(
                interleave.interleave_any_with_lookup_table(
                    0xFFFF, 0x0000, 0xFFFF, 0x0000
                )
            ), '0x55555555'
        )

        integers = (3, 9, 7, 8)
        self.assertEqual(
            hex(interleave.interleave_any_with_lookup_table(*integers)),
            '0xa457'
        )

    def test_interleave4_any_length_input(self):
        integers = (0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF)
        total_integer_length = sum(
            [integer.bit_length() for integer in integers]
        )
        interleaved = self.assertEqual(
            interleave.interleave4_any_length_input(*integers).bit_length(),
            total_integer_length
        )

        integers = (3, 9, 7, 8)
        self.assertEqual(
            interleave.interleave4(*integers),
            interleave.interleave4_any_length_input(*integers)
        )

    def test_deinterleave4_any_length_input(self):
        integers = (0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF)
        self.assertEqual(
            integers,
            interleave.deinterleave4_any_length_input(
                0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            )
        )
        self.assertEqual(
            integers,
            interleave.deinterleave4_any_length_input(
                interleave.interleave4_any_length_input(*integers)
            )
        )
        integers = (15, 12, 999999, 12)
        self.assertEqual(
            integers,
            interleave.deinterleave4_any_length_input(
                interleave.interleave4_any_length_input(*integers)
            )
        )

    def test_interleave_any_16bit_to_any_length_output(self):
        integers = (0xFFFF, 0xFFFF, 0xFFFF, 0xFFFF, 0xFFFF)
        total_integer_length = sum(
            [integer.bit_length() for integer in integers]
        )
        interleaved = self.assertEqual(
            interleave.\
            interleave_any_16bit_to_any_length_output(*integers)\
                .bit_length(),
            total_integer_length
        )
        self.assertEqual(
            interleave.interleave_any_16bit_to_any_length_output(*integers),
            0xFFFFFFFFFFFFFFFFFFFF,
        )
        # this function can only deal with up to 16bit integers; if input
        # integers are > 16bit they are truncated
        integers = (0xFFFFF, 0xFFFFF, 0xFFFFF, 0xFFFFF, 0xFFFFF)
        self.assertEqual(
            interleave.interleave_any_16bit_to_any_length_output(*integers),
            0xFFFFFFFFFFFFFFFFFFFF,
        )

    def test_interleave_any_input_output(self):
        integers = (0xF, 0xF, 0xF)
        total_integer_length = sum(
            [integer.bit_length() for integer in integers]
        )
        interleaved = self.assertEqual(
            interleave.interleave_any_input_output(*integers).bit_length(),
            total_integer_length
        )
        integers = (0xFFFFF, 0xFFFFF, 0xFFFFF, 0xFFFFF)
        self.assertEqual(
            interleave.interleave_any_input_output(*integers),
            0xFFFFFFFFFFFFFFFFFFFF
        )


if __name__ == '__main__':
    unittest.main()
