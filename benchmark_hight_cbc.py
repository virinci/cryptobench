from hight.hight_CBC import cbc_hight_encryption, cbc_hight_decryption


# fmt: off
_MK = [0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89]
_IV = [0x26, 0x8D, 0x66, 0xA7, 0x35, 0xA8, 0x1A, 0x81]
# fmt: on

key_size = len(_MK)
block_size = 8


def encrypt_wrapper(plaintext: bytes) -> bytes:
    return bytes(cbc_hight_encryption(plaintext, _IV, _MK))


def decrypt_wrapper(ciphertext: bytes) -> bytes:
    return bytes(cbc_hight_decryption(ciphertext, _IV, _MK))


source_files = (__file__, "hight/hight_CBC.py", "hight/hight.py")
