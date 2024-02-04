from print import print_cipher
import os
from cryterion import cryterion
import hashlib


THUMBNAIL_SIZE = 32
# fmt: off
# KEY = [0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89]
KEY = [0xC2, 0x88, 0x95, 0xBA, 0x32, 0x7B]
PERMKEY = [0x69, 0xD2, 0xCD, 0xB6]
key = int.from_bytes(KEY, "big")
permkey = int.from_bytes(PERMKEY, "big")
# fmt: on

key_size = len(KEY) + len(PERMKEY)
block_size = 6


def encrypt_wrapper(plaintext: bytes) -> bytes:
    ciphertext = bytearray()
    for i in range(0, len(plaintext), block_size):
        block = int.from_bytes(plaintext[i : i + block_size], "big")
        state = print_cipher.encrypt(block, key, permkey)
        ciphertext.extend(state.to_bytes(block_size))
    return bytes(ciphertext)


def decrypt_wrapper(ciphertext: bytes) -> bytes:
    plaintext = bytearray()
    for i in range(0, len(ciphertext), block_size):
        block = int.from_bytes(ciphertext[i : i + block_size], "big")
        state = print_cipher.decrypt(block, key, permkey)
        plaintext.extend(state.to_bytes(block_size))
    return bytes(plaintext)


source_files = (__file__, "print/print_cipher.py")

if (HOST := os.getenv("RECEIVER")) is not None:
    # HOST = "192.168.166.32"
    PORT = 8000

    P = cryterion.random_text(int(os.getenv("PLAINTEXT")))
    checksum = hashlib.sha256(P).hexdigest()

    P = cryterion.pad(P, block_size)
    C = cryterion.encrypt(
        lambda plaintext: encrypt_wrapper(plaintext),
        P,
        key_size,
        block_size,
        cryterion.code_size_from_files(source_files),
    )

    cryterion.sendall(bytes(C), HOST, PORT)

    print(f"\nPlaintext: {P[:THUMBNAIL_SIZE]}...")
    print(f"Ciphertext: {bytes(C)[:THUMBNAIL_SIZE]}...")
    print(f"Plaintext Checksum: {checksum}")
else:
    HOST = "0.0.0.0"
    PORT = 8000

    C = cryterion.recvall(HOST, PORT)

    D = cryterion.decrypt(
        lambda ciphertext: decrypt_wrapper(ciphertext),
        C,
        key_size,
        block_size,
        cryterion.code_size_from_files(source_files),
    )
    D = cryterion.unpad(D)
    checksum = hashlib.sha256(D).hexdigest()

    print(f"\nCiphertext: {C[:THUMBNAIL_SIZE]}...")
    print(f"Plaintext: {D[:THUMBNAIL_SIZE]}...")
    print(f"Plaintext Checksum: {checksum}")
