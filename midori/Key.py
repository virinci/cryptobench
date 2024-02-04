def round_key_generation(base, key, round_num):
    beta = [
        [3, 5, 7, 8, 10, 11, 14, 15],
        [1, 2, 3, 4, 8, 9],
        [0, 2, 5, 10, 11, 13, 15],
        [1, 2, 6, 11, 14, 15],
        [3, 9, 12, 13, 14, 15],
        [0, 1, 3, 7, 9, 10, 11],
        [6, 9, 10, 13, 14],
        [4, 6, 7, 8, 9, 12, 13],
        [0, 3, 5, 8, 15],
        [1, 8, 10, 11, 12],
        [1, 2, 3, 7, 8, 11, 13, 14, 15],
        [2, 6, 8, 12, 13, 14],
        [1, 3, 7, 10, 11],
        [0, 1, 2, 3, 4, 8, 9, 12, 14],
        [0, 1, 3, 4, 5, 6, 7, 8, 11],
        [1, 2, 3, 4, 5, 8, 15],
        [3, 4, 5, 10, 13],
        [2, 6, 7, 8, 10, 11, 13],
        [1, 2, 6, 8, 12, 14],
    ]
    RK = []
    if base == 64:
        k0 = key[2:18]
        k1 = key[18:]

        if round_num % 2 == 0:
            for i in range(4):
                RK.append([int(k0[i * 4 + j], 16) for j in range(4)])
        else:
            for i in range(4):
                RK.append([int(k1[i * 4 + j], 16) for j in range(4)])
        for ind in beta[round_num]:
            r = ind // 4
            c = ind % 4
            RK[r][c] ^= 1

    else:
        for i in range(4):
            RK.append(
                [int(key[i * 4 + j + 2 : i * 4 + j + 4], 16) for j in range(0, 8, 2)]
            )
        for ind in beta[round_num]:
            r = ind // 4
            c = ind % 4
            RK[r][c] ^= 1
    return RK


def White_Key(key, base):
    if base == 64:
        k0 = key[2:18]
        k1 = key[18:]
        WK = [[0] * 4 for i in range(4)]
        WK0 = []
        WK1 = []
        for i in range(4):
            WK0.append([int(k0[i * 4 + j], 16) for j in range(4)])
        for i in range(4):
            WK1.append([int(k1[i * 4 + j], 16) for j in range(4)])
        for i in range(4):
            for j in range(4):
                WK[i][j] = WK0[i][j] ^ WK1[i][j]
        return WK
    else:
        WK = []
        for i in range(4):
            WK.append(
                [int(key[i * 4 + j + 2 : i * 4 + j + 4], 16) for j in range(0, 8, 2)]
            )
        return WK
