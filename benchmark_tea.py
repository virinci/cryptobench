import tea.tea as tea
import os
from cryterion import cryterion
import hashlib


THUMBNAIL_SIZE = 32
# fmt: off
KEY = [0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89]
# fmt: on

key_size = len(KEY)
block_size = 8


def encrypt_wrapper(plaintext: bytes):
    return tea.encrypt(plaintext, KEY)


def decrypt_wrapper(ciphertext: bytes):
    return tea.decrypt(ciphertext, KEY)


source_files = (__file__, "tea/tea.py")


def sender(host: str, port: int) -> Cryterion:
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

    cryterion.sendall(bytes(C), host, port)
    print(f"\nPlaintext: {P[:THUMBNAIL_SIZE]}...")
    print(f"Ciphertext: {bytes(C)[:THUMBNAIL_SIZE]}...")
    print(f"Plaintext Checksum: {checksum}")


def receiver(host: str, port: int) -> Cryterion:
    C = cryterion.recvall(host, port)

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


if __name__ == "__main__":
    PORT = 8000
    if (HOST := os.getenv("RECEIVER")) is not None:
        sender(HOST, PORT)
    else:
        HOST = "0.0.0.0"
        receiver(HOST, PORT)
