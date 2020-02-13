
from . import galois_field_arithmetic as gf_arithmetic
from . import constants as constants

def dump(block):
    for word in block:
        a = hex(word[0] << 24 | word[1] << 16 | word[2] << 8 | word[3])
        print(a)
    print("")

def number_of_rounds(key: bytearray) -> int:
    """
    """
    if valid_key_size(key):
        return 6 + len(key) // constants.BYTES_PER_KEY_ROW
    
    return (len(key) // 4) - 1


def valid_key_size(key: bytearray) -> bool:
	"""
	"""
	return len(key) == 16 or len(key) == 24 or len(key) == 32

def rot_word(w: []) -> []:
    """
        Performs a simple cyclic permutation.
    """
    return w[1: len(w)] + w[0:1]
    
def key_expansion(key: bytearray) -> []:
    """ Expand a key from 16, 24 or 32 bytes to 176, 208 or 240 bytes.

    """
    num_rounds = number_of_rounds(key)
    
    expanded_key = [None] * (constants.BYTES_PER_KEY_ROW * (num_rounds + 1))
    
    num_words = len(key) // constants.BYTES_PER_KEY_ROW

    for i in range(num_words):
        expanded_key[i] = [ key[i * 4], key[i * 4 + 1], key[i * 4 + 2], key[i * 4 + 3] ]
    

    for i in range(num_words, len(expanded_key)):
        temp = expanded_key[i - 1]

        if i % num_words == 0:
            temp  = xor_words(sub_word(rot_word(temp)), constants.RCON[ i // num_words - 1])

        elif(num_words > 6 and i % num_words == 4):
            temp = sub_word(temp)

        expanded_key[i] = xor_words(expanded_key[i - num_words], temp)


    return expanded_key

def sub_word(w: []) -> []:
    return [ constants.SBOX[n] for n in w]

def sub_bytes(state: []):
    for i in range(len(state)):
        state[i] = sub_word(state[i])

def shift(state: [], n):
    print(n, list(range(n)))
    for i in range(n):
        cp = state[0][i]

        state[0][i + 1] = state[1][i + 1]
        state[1][i + 1] = state[2][i + 1]
        state[2][i + 1] = state[3][i + 1]
        state[3][i + 1] = cp

    print()
    dump(state)

def shift_rows(state: []):
    """ Apply row shifting in a block (16 bytes, 128 bits).
    """
    for i in range(constants.BYTES_PER_BLOCK_ROW):
        shift(state, i)

def mix_columns(state: []):

    for i in range(len(state)):
        a = state[i][:]

        state[i][0] = gf_arithmetic.multiply(2, a[0]) ^ gf_arithmetic.multiply(3, a[1]) ^ a[2] ^ a[3]
        state[i][1] = gf_arithmetic.multiply(2, a[1]) ^ gf_arithmetic.multiply(3, a[2]) ^ a[0] ^ a[3]
        state[i][2] = gf_arithmetic.multiply(2, a[2]) ^ gf_arithmetic.multiply(3, a[3]) ^ a[0] ^ a[1]
        state[i][3] = gf_arithmetic.multiply(2, a[3]) ^ gf_arithmetic.multiply(3, a[0]) ^ a[1] ^ a[2]

def xor_words(w1: [], w2: []) -> []:
    """
    """
    
    if len(w1) != len(w2):
        raise Exception('can\'t XOR two words of different byte lengths.')

    return [ w1[i] ^ w2[i] for i in range(len(w1))]

def add_round_key(state: [], key_block: []):
    for i in range(4):
        state[i] = xor_words(state[i], key_block[i])


def cipher(state: [], w: []) -> []:    
    """
    """

    n_rounds = number_of_rounds(w)
    add_round_key(state, w[0 : constants.BYTES_PER_KEY_ROW])
    

    for r in range(1, n_rounds):
        sub_bytes(state)
        dump(state)
        shift_rows(state)
        dump(state)
        return
        mix_columns(state)
        add_round_key(state, w[r * constants.BYTES_PER_KEY_ROW : (r + 1) * constants.BYTES_PER_KEY_ROW])
    
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, w[n_rounds * constants.BYTES_PER_KEY_ROW : (n_rounds + 1) * constants.BYTES_PER_KEY_ROW])

    return state

def inverse_shift_rows(state: []):
    pass

def inverse_sub_bytes(state: []):
    pass

def inverse_mix_columns(state: []):
    pass

def inverse_cipher(state: [], w: []) -> []:
    
    number_of_rounds = number_of_rounds(w)
    add_round_key(state, w[0 : constants.BYTES_PER_KEY_ROW])

    for r in range(number_of_rounds - 1, 0, -1):
        inverse_shift_rows(state)
        inverse_sub_bytes(state)
        add_round_key(state, w[r * constants.BYTES_PER_KEY_ROW, (r + 1) * (constants.BYTES_PER_KEY_ROW)])
        inverse_mix_columns(state)
    
    inverse_shift_rows(state)
    inverse_sub_bytes(state)
    add_round_key(state, w[0, constants.BYTES_PER_KEY_ROW])

    return state