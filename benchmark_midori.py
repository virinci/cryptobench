from midori.encrypt import encrypt as midori_encrypt
from midori.decrypt import decrypt as midori_decrypt


_MODE = "ECB"
# fmt: off
_KEY = [0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89]
# fmt: on

key_size = len(_KEY)
block_size = 16


def encrypt_wrapper(plaintext: bytes):
    key = "0x" + bytes(_KEY).hex()
    ciphertext = bytearray()

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i : i + block_size]
        state = midori_encrypt(block.decode("charmap"), key, block_size * 8)
        ciphertext.extend(state[i][j] for i in range(4) for j in range(4))

    return bytes(ciphertext)


def decrypt_wrapper(ciphertext: bytes):
    key = "0x" + bytes(_KEY).hex()
    plaintext = bytearray()

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i : i + block_size]
        state = [[block[i * 4 + j] for j in range(4)] for i in range(4)]
        state = midori_decrypt(state, key, block_size * 8)
        plaintext.extend(state[i][j] for i in range(4) for j in range(4))

    return bytes(plaintext)


source_files = (__file__, "midori/encrypt.py", "midori/decrypt.py")
