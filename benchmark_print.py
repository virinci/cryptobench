from print import print_cipher


# fmt: off
_KEY = [0xC2, 0x88, 0x95, 0xBA, 0x32, 0x7B]
_PERMKEY = [0x69, 0xD2, 0xCD, 0xB6]
_key = int.from_bytes(_KEY, "big")
_permkey = int.from_bytes(_PERMKEY, "big")
# fmt: on

key_size = len(_KEY) + len(_PERMKEY)
block_size = 6


def encrypt_wrapper(plaintext: bytes) -> bytes:
    ciphertext = bytearray()
    for i in range(0, len(plaintext), block_size):
        block = int.from_bytes(plaintext[i : i + block_size], "big")
        state = print_cipher.encrypt(block, _key, _permkey)
        ciphertext.extend(state.to_bytes(block_size))
    return bytes(ciphertext)


def decrypt_wrapper(ciphertext: bytes) -> bytes:
    plaintext = bytearray()
    for i in range(0, len(ciphertext), block_size):
        block = int.from_bytes(ciphertext[i : i + block_size], "big")
        state = print_cipher.decrypt(block, _key, _permkey)
        plaintext.extend(state.to_bytes(block_size))
    return bytes(plaintext)


source_files = (__file__, "print/print_cipher.py")
