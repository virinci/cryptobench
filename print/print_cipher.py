def num2bits(num: int, bitlength: int) -> list[int]:
    bits = []
    for i in range(bitlength):
        bits.append(num & 1)
        num >>= 1
    return bits


def bits2num(bits: list[int]) -> int:
    num = 0
    for i, x in enumerate(bits):
        assert x == 0 or x == 1
        num += x << i
    return num


def _update_round_counter(counter: list[int]) -> list[int]:
    t = 1 ^ counter[-1] ^ counter[-2]
    counter.pop()
    counter.insert(0, t)
    return counter


_sbox = (
    (0, 1, 3, 6, 7, 4, 5, 2),
    (0, 1, 7, 4, 3, 6, 5, 2),
    (0, 3, 1, 6, 7, 5, 4, 2),
    (0, 7, 3, 5, 1, 4, 6, 2),
)


def encrypt(plaintext, long_key, short_key, block_bits=48):
    assert block_bits in {48, 96}

    # Compute length for counter.
    if block_bits == 48:
        counter = [0, 0, 0, 0, 0, 0]
    elif block_bits == 96:
        counter = [0, 0, 0, 0, 0, 0, 0]
    else:
        import sys

        sys.stderr.write("ERROR: invalid block_bits\n")
        sys.exit(-1)

    text = num2bits(plaintext, block_bits)
    round_key = num2bits(long_key, block_bits)
    perm_key = num2bits(short_key, block_bits * 2 // 3)

    state = [None] * block_bits  # temp variable
    for round_i in range(block_bits):
        # key xor
        for i in range(block_bits):
            text[i] ^= round_key[i]

        # linear diffusion
        for i in range(block_bits - 1):
            state[(3 * i) % (block_bits - 1)] = text[i]
        state[block_bits - 1] = text[block_bits - 1]

        # round counter
        counter = _update_round_counter(counter)
        for i, x in enumerate(counter):
            state[i] ^= x

        # keyed sbox
        for i in range(block_bits // 3):
            before = bits2num(state[(3 * i) : (3 * i + 3)])
            after = num2bits(_sbox[bits2num(perm_key[2 * i : 2 * i + 2])][before], 3)
            for j in range(3):
                text[3 * i + j] = after[j]

    return bits2num(text)


def decrypt(ciphertext, long_key, short_key, block_bits=48):
    assert block_bits in {48, 96}

    # Compute length for counter
    if block_bits == 48:
        counter = [0, 0, 0, 0, 0, 0]
    elif block_bits == 96:
        counter = [0, 0, 0, 0, 0, 0, 0]

    iterations = block_bits

    counters = []

    for i in range(iterations):
        counter = _update_round_counter(counter.copy())
        counters.append(counter)

    text = num2bits(ciphertext, block_bits)
    round_key = num2bits(long_key, block_bits)
    perm_key = num2bits(short_key, block_bits * 2 // 3)

    state = [None] * block_bits  # temp variable

    for round in range(iterations):
        for i in range(block_bits // 3):
            after = bits2num(text[3 * i : 3 * i + 3])
            row = bits2num(perm_key[2 * i : 2 * i + 2])

            column = -1
            for j in range(len(_sbox[row])):
                if _sbox[row][j] == after:
                    column = j
                    break

            before = num2bits(column, 3)
            for k in range(3):
                state[3 * i + k] = before[k]

        for county in range(len(counters[iterations - round - 1])):
            state[county] = state[county] ^ counters[iterations - round - 1][county]

        for i in range(block_bits - 1):
            text[i] = state[(3 * i) % (block_bits - 1)]
        text[block_bits - 1] = state[block_bits - 1]

        for i in range(block_bits):
            text[i] ^= round_key[i]

    return bits2num(text)


if __name__ == "__main__":
    plaintext = 0x4C847555C35B
    key = 0xC28895BA327B
    permkey = 0x69D2CDB6

    ciphertext = encrypt(plaintext, key, permkey)

    print("plain =", hex(plaintext))
    print("key =", hex(key))
    print("permkey =", hex(permkey))
    print("cipher =", hex(ciphertext))

    plaintext = decrypt(ciphertext, key, permkey)
    print("plain =", hex(plaintext))
