import os
import base64

from . import constants as cons
from . import rijndael

def read_data(file_path):
    f = open(file_path, 'rb')
    data = bytearray(f.read())
    f.close()

    no_blocks = (len(data) + (len(data) % 16)) // (cons.BLOCK_SIZE_BYTES)

    blocks = [None] * no_blocks

    n = 0

    for i in range(no_blocks):
        
        blocks[i] = [None] * cons.BYTES_PER_BLOCK_ROW

        for j in range(cons.BYTES_PER_BLOCK_ROW):

            blocks[i][j] = [None] * cons.BYTES_PER_BLOCK_ROW

            for k in range(cons.BYTES_PER_BLOCK_ROW):
                
                if n < len(data):
                    blocks[i][j][k] = data[n]
                else:
                    blocks[i][j][k] = 0x0
                n += 1

    return blocks

def xor_blocks(b1: [], b2: []) -> []:
    return [ rijndael.xor_words(bi, bj) for bi,bj in zip(b1, b2)]

def generate_random_initialization_value() -> []:
	"""
	"""
	rb = bytearray(os.urandom(cons.BLOCK_SIZE_BYTES))
	return [ [ rb[4 * i + j] for j in range(cons.BYTES_PER_BLOCK_ROW)] for i in range(cons.BYTES_PER_BLOCK_ROW)]

def encrypt_blocks(blocks: [], expanded_key: [], iv: []) -> []:

    for i in range(0, len(blocks)):
        if i > 0:
            iv = blocks[i - 1]
        
        blocks[i] = xor_blocks(blocks[i], iv)
        blocks[i] = rijndael.cipher(blocks[i], expanded_key)
    
    return blocks

def block_to_byte_array(block: []) -> bytearray:
    a = [None] * cons.BLOCK_SIZE_BYTES
    i = 0

    for word in block:
        for b in word:
            a[i] = b
            i += 1
    
    return bytearray(a)

def encrypt_file(input_file_path: str,  output_file_path: str, key: bytearray, iv=generate_random_initialization_value()):
        in_blocks = read_data(input_file_path)

        out_blocks = encrypt_blocks(in_blocks, rijndael.key_expansion(key), iv)

        out_file = open(output_file_path, 'wb')

        a = block_to_byte_array(iv)

        for b in out_blocks:
            a += block_to_byte_array(b)        
                
        out_file.write(base64.b64encode(a))
        out_file.close()


def decrypt_file(input_file_path: str, output_file_path: str, key: bytearray):
    in_blocks = read_data(input_file_path)