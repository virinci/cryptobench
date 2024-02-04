import random

from encrypt import *
from decrypt import *


def print_stmt(code, state):
    if code == 0:
        digest = "0x"
        for i in range(4):
            for j in range(4):
                digest += hex(state[i][j])[2:]
        print("Encrypted Text: ", digest)
    else:
        text = ""
        for i in range(4):
            for j in range(4):
                text += chr(state[i][j])
        print("Decrypted Text: ", text)


hash = random.getrandbits(128)
key = hex(hash)


msg = input("Enter message (max 16 characters) :")
print("Key Generated: ", key)
msg = msg.ljust(16, "0")

state = encrypt(msg, key, 128)
print_stmt(0, state)
state = decrypt(state, key, 128)
print_stmt(1, state)
