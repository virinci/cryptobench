import os
from cryterion import Cryterion
import cryterion
from benchmark import benchmark_sender, benchmark_receiver
from importlib import import_module
import socket
from typing import Any
import random


def sendall_to_socket(data: bytes, s):
    s.sendall(data)


def recvall_from_socket(conn, max_bufsize=100 * 1024) -> bytes:
    received = b""

    while True:
        data = conn.recv(4096)
        received += data
        if len(data) != 4096 or len(received) >= max_bufsize:
            break

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

    # load all algo modules in an array
    loaded_modules = {}
    for algo in ALGOS:
        loaded_modules[algo] = import_module(f"benchmark_{algo}")

    print(loaded_modules)
    PORT = 8823

    if (HOST := os.getenv("RECEIVER")) is not None:
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
            print(f"trying to send name of {algo = } to  {HOST = } {PORT = }")
            # cryterion.sendall(item.encode(), HOST, PORT)
            sendall_to_socket(algo.encode(), s)

            ack = recvall_from_socket(conn)
            assert ack == b"ACK"

            # wait for acknowledgement from receiver
            # algo = cryterion.recvall(HOST, PORT + 1)
            # print(algo)
            benchmarks = benchmark_sender(
                loaded_modules[algo],
                lambda c: sendall_to_socket(c, s),
            )
            ack = recvall_from_socket(conn)
            assert ack == b"ACK"

        while True:
            algo = random.choice(ALGOS)
            # Send name of algo to receiver
            print(f"trying to send name of {algo = } to  {HOST = } {PORT = }")
            # cryterion.sendall(item.encode(), HOST, PORT)
            sendall_to_socket(algo.encode(), s)

            ack = recvall_from_socket(conn)
            assert ack == b"ACK"

            # wait for acknowledgement from receiver
            # algo = cryterion.recvall(HOST, PORT + 1)
            # print(algo)
            benchmarks = benchmark_sender(
                loaded_modules[algo],
                lambda c: sendall_to_socket(c, s),
            )
            ack = recvall_from_socket(conn)
            assert ack == b"ACK"
        # print(benchmarks)
        # add data to table
        # benchmark_sender(benchmark_module, HOST, PORT)
        # find rank 1 from table
        # send name of algo to receiver
        # wait for ack
        # benchmark_sender(algo,H,P)
        # update table
        s.close()
    else:
        # receiver's section

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
            algo_name_bytes = conn.recv(1024)
            print(f"Received name {algo_name_bytes = }")
            algo: str = algo_name_bytes.decode()
            sendall_to_socket(b"ACK", s2)
            print(f"{algo = }")

            print(f"Now to receive: {algo}")
            benchmark_receiver(loaded_modules[algo], lambda: recvall_from_socket(conn))
            sendall_to_socket(b"ACK", s2)
