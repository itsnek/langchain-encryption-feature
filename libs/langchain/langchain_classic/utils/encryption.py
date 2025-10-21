from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def encrypt(user_input: str) -> str:
    key = b'\x17\xf1o\x04\x08\x1c\x1b\x0e\x8a%\xbc\xa7\x05\xb4\x8e\x01'
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(user_input.encode())

    return ciphertext
