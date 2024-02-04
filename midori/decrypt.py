from .sbox import *
from .linear import *
from .Key import *


def decrypt(state, key, base):
    WK = White_Key(key, base)
    KeyAdd(state, WK)
    t_round = 16
    if base == 128:
        t_round = 20
    for round in range(t_round - 2, -1, -1):
        sbox(state, base)
        MixColumn(state)
        InvShuffleCell(state)
        RKi = round_key_generation(base, key, round)
        MixColumn(RKi)
        InvShuffleCell(RKi)
        KeyAdd(state, RKi)
    sbox(state, base)
    KeyAdd(state, WK)
    return state
