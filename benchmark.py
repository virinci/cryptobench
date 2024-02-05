"""A benchmark module is required to expose:
key_size, block_size, encrypt_wrapper, decrypt_wrapper, source_files
"""

import os
import cryterion
import hashlib
from collections.abc import Callable


THUMBNAIL_SIZE = 32


def benchmark_sender(module, send_fn: Callable[[bytes], None]) -> cryterion.Cryterion:
    P = cryterion.random_text(int(os.getenv("PLAINTEXT") or 10_000))
    checksum = hashlib.sha256(P).hexdigest()

    P = cryterion.pad(P, module.block_size)
    C, benchmark_result = cryterion.benchmark_fn(
        module.encrypt_wrapper,
        P,
        module.key_size,
        module.block_size,
        cryterion.code_size_from_files(module.source_files),
    )

    send_fn(C)
    print(f"Plaintext: {P[:THUMBNAIL_SIZE]}...")
    print(f"Ciphertext: {C[:THUMBNAIL_SIZE]!r}...")
    print(f"Plaintext Checksum: {checksum}")

    return benchmark_result


def benchmark_receiver(module, recv_fn: Callable[[], bytes]) -> cryterion.Cryterion:
    C = recv_fn()

    D, benchmark_result = cryterion.benchmark_fn(
        module.decrypt_wrapper,
        C,
        module.key_size,
        module.block_size,
        cryterion.code_size_from_files(module.source_files),
    )
    D = cryterion.unpad(D)
    checksum = hashlib.sha256(D).hexdigest()

    print(f"Ciphertext: {C[:THUMBNAIL_SIZE]!r}...")
    print(f"Plaintext: {D[:THUMBNAIL_SIZE]}...")
    print(f"Plaintext Checksum: {checksum}")

    return benchmark_result


def benchmark_sender_after_connecting(
    module, host: str, port: int
) -> cryterion.Cryterion:
    return benchmark_sender(module, lambda c: cryterion.sendall(c, host, port))


def benchmark_receiver_after_connecting(
    module, host: str, port: int
) -> cryterion.Cryterion:
    return benchmark_receiver(module, lambda: cryterion.recvall(host, port))


if __name__ == "__main__":
    import benchmark_ascon as benchmark_module

    PORT = 8000
    if (HOST := os.getenv("RECEIVER")) is not None:
        benchmark_sender_after_connecting(benchmark_module, HOST, PORT)
    else:
        HOST = "0.0.0.0"
        benchmark_receiver_after_connecting(benchmark_module, HOST, PORT)
