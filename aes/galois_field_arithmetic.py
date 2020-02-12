import math

from . import constants as c

def find_greatest_bit_position(num):
    m = 0

    for i in range(int((math.log2(num))) + 1):
        if num & (1 << i) > 0:
            m = i

    return m

def modulo_irreducible_polynomial(pol):
    """
	"""
    while pol >= c.X_8_POLYNOMIAL: pol = pol ^ ( c.IRREDUCIBLE_POL <<  max(0, find_greatest_bit_position(pol) - 8))

    return pol

def multiply(a, b):
	"""
		https://www.wikiwand.com/en/Finite_field_arithmetic#/C_programming_example
	"""
	c = 0
	if (a & 1) == 1:
		c = b

	for _ in range(1, 8):
		hi_bit = (b & 0x80)
		b <<= 1
		b &= 0xff
		if hi_bit == 0x80:
			b ^= 0x1b
		a >>= 1
		if (a & 1) == 1:
			c ^= b
	return c

