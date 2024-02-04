from .sbox import *
from .linear import *
from .Key import *


def encrypt(msg, key, base):
    state = [[0] * 4 for i in range(4)]
    for i in range(16):
        r = i // 4
        c = i % 4
        state[r][c] = ord(msg[i])
    WK = White_Key(key, base)
    KeyAdd(state, WK)
    t_round = 16
    if base == 128:
        t_round = 20
    for round in range(t_round - 1):
        sbox(state, base)
        ShuffleCell(state)
        MixColumn(state)
        KeyAdd(state, round_key_generation(base, key, round))
    sbox(state, base)
    KeyAdd(state, WK)
    return state
