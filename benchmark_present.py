from present.pypresent import Present


# fmt: off
_KEY = [0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89]
# fmt: on

key_size = len(_KEY)

_cipher = Present(_KEY)
block_size = _cipher.get_block_size()


def encrypt_wrapper(plaintext: bytes):
    cipher = Present(_KEY)
    ciphertext = bytearray()

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i : i + block_size]
        ciphertext.extend(cipher.encrypt(block))

    return bytes(ciphertext)


def decrypt_wrapper(ciphertext: bytes):
    cipher = Present(_KEY)
    plaintext = bytearray()

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i : i + block_size]
        plaintext.extend(cipher.decrypt(block))

    return bytes(plaintext)


source_files = (__file__, "present/pypresent.py")
