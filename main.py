import argparse

import aes

parser = argparse.ArgumentParser(description='Encryt or Decrypt a file using AES cipher.')

parser.add_argument('--key-file', type=str, help='')
parser.add_argument('--in-file', type=str, help='', required=True)
parser.add_argument('--out-file', type=str, help='', required=True)

def main():
    args = parser.parse_args()
    
    key = None

    if args.key_file:
        key = aes.read_private_key_file(args.key_file)
    else:
        key = aes.generate_private_key(aes.SIZE_256_BIT_KEY_IN_BYTES)

    aes.cbc.encrypt_file(args.in_file, args.out_file, key)
                   

if __name__ == "__main__":
    main()