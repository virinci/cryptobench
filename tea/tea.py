"""Implementation of the Tiny Encryption Algorithm (TEA) for Python
https://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm

Example Usage:

import tea

# The key must be 16 characters.
key = b'0123456789abcdef'
message = b'Sample message for encryption and decryption.'

cipher = tea.encrypt(message, key)
assert message == tea.decrypt(cipher, key)
"""

import ctypes
import itertools


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    """Encrypts a message using a 16-character key."""
    if len(plaintext) == 0:
        return b""

    v = _str2vec(plaintext)
    k = _str2vec(key)

    bytearray = b"".join(_vec2str(_encipher(chunk, k)) for chunk in _chunks(v, 2))
    return bytearray


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypts a message using a 16-character key."""
    if not ciphertext:
        return ""

    assert len(key) == 16
    v = _str2vec(ciphertext)
    k = _str2vec(key)

    return b"".join(_vec2str(_decipher(chunk, k)) for chunk in _chunks(v, 2))


def _encipher(v, k):
    """TEA encipher algorithm.
    Encodes a length-2 vector using a length-4 vector as a length-2 vector.

    :param v:
        A vector representing the information to be enciphered.  *Must* have a length of 2.
    :param k:
        A vector representing the encryption key.  *Must* have a length of 4.
    :return:
        A length-2 vector representing the encrypted information v.
    """
    y, z = [ctypes.c_uint32(x) for x in v]
    sum = ctypes.c_uint32(0)
    delta = 0x9E3779B9

    for n in range(32, 0, -1):
        sum.value += delta
        y.value += (z.value << 4) + k[0] ^ z.value + sum.value ^ (z.value >> 5) + k[1]
        z.value += (y.value << 4) + k[2] ^ y.value + sum.value ^ (y.value >> 5) + k[3]

    return [y.value, z.value]


def _decipher(v, k):
    """
    TEA decipher algorithm.  Decodes a length-2 vector using a length-4 vector as a length-2 vector.

    Compliment of _encipher.

    :param v:
        A vector representing the information to be deciphered.  *Must* have a length of 2.
    :param k:
        A vector representing the encryption key.  *Must* have a length of 4.
    :return:
        The original message.
    """
    y, z = [ctypes.c_uint32(x) for x in v]
    sum = ctypes.c_uint32(0xC6EF3720)
    delta = 0x9E3779B9

    for n in range(32, 0, -1):
        z.value -= (y.value << 4) + k[2] ^ y.value + sum.value ^ (y.value >> 5) + k[3]
        y.value -= (z.value << 4) + k[0] ^ z.value + sum.value ^ (z.value >> 5) + k[1]
        sum.value -= delta

    return [y.value, z.value]


def _chunks(iterable, n):
    """Iterates through an iterable in chunks of size n."""
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def _str2vec(value, l=4):
    """Encodes a binary string as a vector.  The string is split into chunks of length l and each chunk is encoded as 2 elements in the return value."""
    # Split the string into chunks.
    chunks = [value[i : i + l] for i in range(0, len(value), l)]

    return [sum(c << 8 * i for i, c in enumerate(chunk)) for chunk in chunks]


def _vec2str(vector, l=4):
    """Decodes a vector to a binary string. The string is composed by chunks of size l for every two elements in the vector."""
    return bytes((element >> 8 * i) & 0xFF for element in vector for i in range(l))
