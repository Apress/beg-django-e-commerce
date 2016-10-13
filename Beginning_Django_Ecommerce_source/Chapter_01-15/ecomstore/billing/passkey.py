from keyczar import keyczar
import os

#KEY_PATH = /system/path/to/keys/

def encrypt(plaintext):
    crypter = _get_crypter()
    return crypter.Encrypt(plaintext)

def decrypt(ciphertext):
    crypter = _get_crypter()
    return crypter.Decrypt(ciphertext)

def _get_crypter():
    return keyczar.Crypter.Read(KEY_PATH)


