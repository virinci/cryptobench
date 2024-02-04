from ascon import ascon


_key = b"\xd2\x93\x10=9\xea\xd4&\x9f8Z\x04'\x17\xd6D"
_nonce = b"\xc9R\xe9\xce\x05S\x99T\xd4\xa0\xd4tP)\xc6\xf0"
_associateddata = b"ANY RANDOM DATA"
_variant = "Ascon-128"

key_size = len(_key)
block_size = 1


def encrypt_wrapper(plaintext: bytes) -> bytes:
    return ascon.ascon_encrypt(_key, _nonce, _associateddata, plaintext, _variant)


def decrypt_wrapper(ciphertext: bytes) -> bytes:
    return ascon.ascon_decrypt(_key, _nonce, _associateddata, ciphertext, _variant)


source_files = (__file__, "ascon/ascon.py")
