import os
import math
import base64

from . import cbc
from . import rijndael


def generate_random_bytes(num_bytes: int) -> bytearray:
	"""
	"""
	return bytearray(os.urandom(num_bytes))

def generate_private_key(key_size_in_bytes : int) -> bytearray:
	"""
	"""
	return bytearray(generate_random_bytes(key_size_in_bytes))

def read_private_key_file(key_file_path: str) -> bytearray:
	"""
	"""
	if os.path.isfile(key_file_path):
		key = bytearray(open(key_file_path, "rb").read())
        
		if not rijndael.valid_key_size(key):
			raise Exception('Invalid key size.')
		
		return key
	
	else:
		raise Exception('Invalid private key path.')