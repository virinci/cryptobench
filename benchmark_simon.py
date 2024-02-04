from simon.simon import SimonCipher
import os
from cryterion import cryterion
import hashlib


MODE = "ECB"
THUMBNAIL_SIZE = 32
# fmt: off
KEY = [0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89]
# fmt: on

key_size = len(KEY)
block_size = 8
cipher = SimonCipher(
    cryterion.int_from_bytes(bytes(KEY)),
    key_size=key_size * 8,
    block_size=block_size * 8,
    mode=MODE,
)


def simon_encrypt(plaintext: bytes):
    ciphertext = 0

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i : i + block_size]
        ciphertext <<= 8 * block_size
        ciphertext |= cipher.encrypt(cryterion.int_from_bytes(block))

    return cryterion.int_to_bytes(ciphertext)


def simon_decrypt(ciphertext: bytes):
    plaintext = 0

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i : i + block_size]
        plaintext <<= 8 * block_size
        plaintext |= cipher.decrypt(cryterion.int_from_bytes(block))

    return cryterion.int_to_bytes(plaintext)


source_files = (__file__, "simon/simon.py")

if (HOST := os.getenv("RECEIVER")) is not None:
    # HOST = "192.168.166.32"
    PORT = 8000

    P = cryterion.random_text(int(os.getenv("PLAINTEXT")))
    checksum = hashlib.sha256(P).hexdigest()

    P = cryterion.pad(P, block_size)
    C = cryterion.encrypt(
        lambda plaintext: simon_encrypt(plaintext),
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
        lambda ciphertext: simon_decrypt(ciphertext),
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
