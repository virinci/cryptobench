from klein.klein import KLEIN


_KEY = [226, 228, 119, 27, 80, 75, 166, 104]
_key = int.from_bytes(_KEY, "big")

key_size = len(_KEY)
block_size = 8

_klein = KLEIN(size=block_size * 8)


def encrypt_wrapper(plaintext: bytes) -> bytes:
    # return _klein.encrypt(_key, int.from_bytes(plaintext, "big")).to_bytes(len(plaintext))
    ciphertext = bytearray()
    for i in range(0, len(plaintext), block_size):
        block = int.from_bytes(plaintext[i : i + block_size], "big")
        state = _klein.encrypt(_key, block)
        ciphertext.extend(state.to_bytes(block_size))
    return bytes(ciphertext)


def decrypt_wrapper(ciphertext: bytes) -> bytes:
    # return _klein.encrypt(_key, int.from_bytes(ciphertext, "big")).to_bytes(len(ciphertext))
    plaintext = bytearray()
    for i in range(0, len(ciphertext), block_size):
        block = int.from_bytes(ciphertext[i : i + block_size], "big")
        state = _klein.encrypt(_key, block)
        plaintext.extend(state.to_bytes(block_size))
    return bytes(plaintext)


source_files = (__file__, "klein/klein.py")
