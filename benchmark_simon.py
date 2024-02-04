from simon.simon import SimonCipher


_MODE = "ECB"
# fmt: off
_KEY = [0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89]
# fmt: on

key_size = len(_KEY)
block_size = 8

_cipher = SimonCipher(
    cryterion.int_from_bytes(bytes(_KEY)),
    key_size=key_size * 8,
    block_size=block_size * 8,
    mode=_MODE,
)


def encrypt_wrapper(plaintext: bytes) -> bytes:
    ciphertext = 0

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i : i + block_size]
        ciphertext <<= 8 * block_size
        ciphertext |= _cipher.encrypt(cryterion.int_from_bytes(block))

    return cryterion.int_to_bytes(ciphertext)


def decrypt_wrapper(ciphertext: bytes) -> bytes:
    plaintext = 0

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i : i + block_size]
        plaintext <<= 8 * block_size
        plaintext |= _cipher.decrypt(cryterion.int_from_bytes(block))

    return cryterion.int_to_bytes(plaintext)


source_files = (__file__, "simon/simon.py")
