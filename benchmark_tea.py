import tea.tea as tea


# fmt: off
KEY = [0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89]
# fmt: on

key_size = len(KEY)
block_size = 8


def encrypt_wrapper(plaintext: bytes) -> bytes:
    return tea.encrypt(plaintext, KEY)


def decrypt_wrapper(ciphertext: bytes) -> bytes:
    return tea.decrypt(ciphertext, KEY)


source_files = (__file__, "tea/tea.py")
