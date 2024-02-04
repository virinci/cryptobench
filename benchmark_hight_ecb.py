from hight.hight_ECB import ecb_hight_encryption, ecb_hight_decryption
import os
from cryterion import cryterion
import hashlib


THUMBNAIL_SIZE = 32


# TEST CASE
# fmt: off
MK = [0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89]
# fmt: on

source_files = (__file__, "hight/hight_ECB.py", "hight/hight.py")
block_size = 8

if (HOST := os.getenv("RECEIVER")) is not None:
    # HOST = "192.168.166.32"
    PORT = 8000

    P = cryterion.random_text(int(os.getenv("PLAINTEXT")))
    checksum = hashlib.sha256(P).hexdigest()

    P = cryterion.pad(P, block_size)
    C = cryterion.encrypt(
        lambda plaintext: ecb_hight_encryption(plaintext, MK),
        P,
        len(MK),
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
        lambda ciphertext: ecb_hight_decryption(ciphertext, MK),
        C,
        len(MK),
        block_size,
        cryterion.code_size_from_files(source_files),
    )
    D = cryterion.unpad(bytes(D))
    checksum = hashlib.sha256(D).hexdigest()

    print(f"\nCiphertext: {C[:THUMBNAIL_SIZE]}...")
    print(f"Plaintext: {D[:THUMBNAIL_SIZE]}...")
    print(f"Plaintext Checksum: {checksum}")
