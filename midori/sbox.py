def sbox(state, base):
    Sb0 = [
        0xC,
        0xA,
        0xD,
        0x3,
        0xE,
        0xB,
        0xF,
        0x7,
        0x8,
        0x9,
        0x1,
        0x5,
        0x0,
        0x2,
        0x4,
        0x6,
    ]
    Sb1 = [
        0x1,
        0x0,
        0x5,
        0x3,
        0xE,
        0x2,
        0xF,
        0x7,
        0xD,
        0xA,
        0x9,
        0xB,
        0xC,
        0x8,
        0x4,
        0x6,
    ]
    if base == 64:
        for i in range(4):
            for j in range(4):
                state[i][j] = Sb0[state[i][j]]
    else:
        # base 128 construction of SSb_i
        y = []  # input bit permutation
        y.append([4, 1, 6, 3, 0, 5, 2, 7])  # SSb_0
        y.append([1, 6, 7, 0, 5, 2, 3, 4])  # SSb_1
        y.append([2, 3, 4, 1, 6, 7, 0, 5])  # SSb_2
        y.append([7, 4, 1, 2, 3, 0, 5, 6])  # SSb_3
        for i in range(4):
            for j in range(4):
                state_num = i * 4 + j
                bin_state = [
                    bin(state[i][j])[2:].zfill(8)[k] for k in range(8)
                ]  # 8 bit state in binary
                per_state = [bin_state[y[state_num % 4][i]] for i in range(8)]
                # MSB
                MSB = ""
                MSB = Sb1[int(MSB.join(per_state[:4]), 2)]  # Sub byte
                MSB = [bin(MSB)[2:].zfill(4)[i] for i in range(4)]

                # LSB
                LSB = ""
                LSB = Sb1[int(LSB.join(per_state[4:]), 2)]  # Sub byte
                LSB = [bin(LSB)[2:].zfill(4)[i] for i in range(4)]

                # permutation inverse
                MSB.extend(LSB)
                per_state = MSB
                bin_state = [per_state[y[state_num % 4].index(k)] for k in range(8)]
                bin_str = ""
                state[i][j] = int(bin_str.join(bin_state), 2)
