"""A benchmark module is required to expose:
key_size, block_size, encrypt_wrapper, decrypt_wrapper, source_files
"""

import os
from cryterion import cryterion
import hashlib


THUMBNAIL_SIZE = 32


def benchmark_sender(module, host: str, port: int) -> cryterion.Cryterion:
    P = cryterion.random_text(int(os.getenv("PLAINTEXT")))
    checksum = hashlib.sha256(P).hexdigest()

    P = cryterion.pad(P, module.block_size)
    C, benchmark_result = cryterion.benchmark_fn(
        module.encrypt_wrapper,
        P,
        module.key_size,
        module.block_size,
        cryterion.code_size_from_files(module.source_files),
    )

    cryterion.sendall(C, host, port)
    print(f"Plaintext: {P[:THUMBNAIL_SIZE]}...")
    print(f"Ciphertext: {C[:THUMBNAIL_SIZE]}...")
    print(f"Plaintext Checksum: {checksum}")

    return benchmark_result


def benchmark_receiver(module, host: str, port: int) -> cryterion.Cryterion:
    C = cryterion.recvall(host, port)

    D, benchmark_result = cryterion.benchmark_fn(
        module.decrypt_wrapper,
        C,
        module.key_size,
        module.block_size,
        cryterion.code_size_from_files(module.source_files),
    )
    D = cryterion.unpad(D)
    checksum = hashlib.sha256(D).hexdigest()

    print(f"Ciphertext: {C[:THUMBNAIL_SIZE]}...")
    print(f"Plaintext: {D[:THUMBNAIL_SIZE]}...")
    print(f"Plaintext Checksum: {checksum}")

    return benchmark_result


if __name__ == "__main__":
    import benchmark_ascon

    PORT = 8000
    if (HOST := os.getenv("RECEIVER")) is not None:
        benchmark_sender(benchmark_ascon, HOST, PORT)
    else:
        HOST = "0.0.0.0"
        benchmark_receiver(benchmark_ascon, HOST, PORT)
