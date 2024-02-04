from print import print_cipher
import os
from cryterion import cryterion
import hashlib


THUMBNAIL_SIZE = 32
# fmt: off
KEY = [0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89]
# fmt: on

key_size = len(KEY)
block_size = 6


def encrypt_wrapper(plaintext: bytes) -> bytes:
    nbytes = len(plaintext)
    plaintext = int.from_bytes(plaintext, "big")
    long_key = int.from_bytes(KEY, "big")
    short_key = 0x69D2CDB6
    ciphertext = print_cipher.enc(
        plaintext, long_key, short_key, block_bits=block_size * 8
    )
    return ciphertext.to_bytes(nbytes, "big")


def decrypt_wrapper(ciphertext: bytes) -> bytes:
    nbytes = len(ciphertext)
    ciphertext = int.from_bytes(ciphertext, "big")
    long_key = int.from_bytes(KEY, "big")
    short_key = 0x69D2CDB6
    plaintext = print_cipher.enc(
        ciphertext, long_key, short_key, block_bits=block_size * 8
    )
    return plaintext.to_bytes(nbytes, "big")


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
