def ShuffleCell(state):
    per = [0, 10, 5, 15, 14, 4, 11, 1, 9, 3, 12, 6, 7, 13, 2, 8]
    new_state = [[0] * 4 for i in range(4)]
    for i in range(len(state)):
        for j in range(len(state[0])):
            r = per[i * 4 + j] // 4
            c = per[i * 4 + j] % 4
            new_state[i][j] = state[r][c]
    for i in range(len(state)):
        for j in range(len(state[0])):
            state[i][j] = new_state[i][j]


def InvShuffleCell(state):
    per = [0, 7, 14, 9, 5, 2, 11, 12, 15, 8, 1, 6, 10, 13, 4, 3]
    new_state = [[0] * 4 for i in range(4)]
    for i in range(4):
        for j in range(4):
            r = per[i * 4 + j] // 4
            c = per[i * 4 + j] % 4
            new_state[i][j] = state[r][c]
    for i in range(len(state)):
        for j in range(len(state[0])):
            state[i][j] = new_state[i][j]


def MixColumn(state):
    M = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
    new_state = [[0] * 4 for i in range(4)]
    for r in range(4):
        for i in range(4):
            sum = 0
            for j in range(4):
                sum ^= M[i][j] * state[r][j]
            new_state[r][i] = sum
    for i in range(4):
        for j in range(4):
            state[i][j] = new_state[i][j]


# key addition function
def KeyAdd(state, key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= key[i][j]
