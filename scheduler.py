import os
from cryterion import Cryterion
import cryterion
from benchmark import benchmark_sender, benchmark_receiver
from importlib import import_module
import socket
from typing import Any
import random
from outbench import Outbench


def send_sized_to_socket(data: bytes, s):
    length = len(data).to_bytes(4, "big")
    s.sendall(length)
    s.sendall(data)


def recv_sized_from_socket(conn, max_bufsize=100 * 1024) -> bytes:
    length = int.from_bytes(conn.recv(4), "big")
    assert length <= max_bufsize
    received = conn.recv(length)
    assert len(received) == length
    return received


ALGOS = [
    "ascon",
    "hight_cbc",
    "hight_ecb",
    # "klein",
    "midori",
    "present",
    "print",
    "simon",
    "speck",
    "tea",
]

if __name__ == "__main__":
    # Load all algo modules in an array
    loaded_modules = {}
    for algo in ALGOS:
        loaded_modules[algo] = import_module(f"benchmark_{algo}")

    # print(loaded_modules)
    PORT = 8828

    if (HOST := os.getenv("RECEIVER")) is not None:
        outbench = Outbench()

        # Create the sender socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        # Create the receiver socket
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.bind(("0.0.0.0", PORT + 1))
        s2.listen()

        conn, (sender_host, sender_port) = s2.accept()
        print(sender_host, sender_port)

        for algo in ALGOS:
            # Send name of algo to receiver
            print(f"Trying to send name of {algo = } to  {HOST = } {PORT = }")
            send_sized_to_socket(algo.encode(), s)
            assert recv_sized_from_socket(conn) == b"ACK"

            benchmarks = benchmark_sender(
                loaded_modules[algo],
                lambda c: send_sized_to_socket(c, s),
            )
            assert recv_sized_from_socket(conn) == b"ACK"
            outbench.push_benchmarks(algo, benchmarks)

        while True:
            algo = outbench.pick_best(verbose=True)
            # Send name of algo to receiver
            print(f"Trying to send name of {algo = } to  {HOST = } {PORT = }")
            send_sized_to_socket(algo.encode(), s)
            assert recv_sized_from_socket(conn) == b"ACK"

            benchmarks = benchmark_sender(
                loaded_modules[algo],
                lambda c: send_sized_to_socket(c, s),
            )
            assert recv_sized_from_socket(conn) == b"ACK"
            outbench.push_benchmarks(algo, benchmarks)
        s.close()
    else:
        # Create the receiver socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", PORT))
        s.listen()

        conn, (sender_host, sender_port) = s.accept()
        print(sender_host, sender_port)

        # Create the sender socket
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect((sender_host, PORT + 1))

        while True:
            # Wait infinitely till receive name of algo
            algo_name_bytes = recv_sized_from_socket(conn)
            send_sized_to_socket(b"ACK", s2)
            print(f"Received name {algo_name_bytes = }")

            algo: str = algo_name_bytes.decode()
            print(f"{algo = }")

            print(f"Now to receive: {algo}")
            benchmark_receiver(
                loaded_modules[algo], lambda: recv_sized_from_socket(conn)
            )
            send_sized_to_socket(b"ACK", s2)
