from midori.encrypt import encrypt as midori_encrypt
from midori.decrypt import decrypt as midori_decrypt
import os
from cryterion import cryterion
import hashlib


MODE = "ECB"
THUMBNAIL_SIZE = 32
# fmt: off
KEY = [0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89]
# fmt: on

key_size = len(KEY)
block_size = 16


def encrypt_wrapper(plaintext: bytes):
    key = "0x" + bytes(KEY).hex()
    ciphertext = bytearray()

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i : i + block_size]
        state = midori_encrypt(block.decode("charmap"), key, block_size * 8)
        ciphertext.extend(state[i][j] for i in range(4) for j in range(4))

    return bytes(ciphertext)


def decrypt_wrapper(ciphertext: bytes):
    key = "0x" + bytes(KEY).hex()
    plaintext = bytearray()

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i : i + block_size]
        state = [[block[i * 4 + j] for j in range(4)] for i in range(4)]
        state = midori_decrypt(state, key, block_size * 8)
        plaintext.extend(state[i][j] for i in range(4) for j in range(4))

    return bytes(plaintext)


source_files = (__file__, "midori/encrypt.py", "midori/decrypt.py")

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
