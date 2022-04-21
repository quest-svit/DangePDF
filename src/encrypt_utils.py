#!/usr/bin/python env

import base64
import json
import random
import pyaes, pbkdf2, binascii, os, secrets

ENCODING_UTF_8='utf-8'
JSON_KEY_KEY = "key"
JSON_KEY_IV = "iv"
SETTINGS_FILE = "settings.json"

def create_encryption_key(password):
    ''' Derive a 256-bit AES encryption key from the password '''

    SALT_LENGTH = 32
    passwordSalt = os.urandom(SALT_LENGTH)
    key = pbkdf2.PBKDF2(password, passwordSalt).read(SALT_LENGTH)
    return key



def encrypt(plaintext, key,iv):
    ''' Encrypt the plaintext with the given key'''

    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    return aes.encrypt(plaintext)


def decrypt(ciphertext,key,iv):
    ''' Decrypt the ciphertext with the given key '''

    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    return aes.decrypt(ciphertext)

def encode_for_json_compatibility(key):
    '''JSON only supports UTF-8 characters where as the KEY generated is a bytes data-type
    Hence we need to convert to UTF-8 for storing in JSON'''

    return binascii.hexlify(key).decode(ENCODING_UTF_8)

def decode_key_from_json(json_key_value):
    '''JSON only supports UTF-8 characters where as the KEY generated is a bytes data-type
    Hence we need to convert back to bytes for decryption'''

    return binascii.unhexlify(json_key_value.encode(ENCODING_UTF_8))

def create_settings_json(key,iv):
    ''' Create the settings.json file to store encryption Key'''

    settings = {}
    settings[JSON_KEY_KEY]= encode_for_json_compatibility(key)
    settings[JSON_KEY_IV]= iv

    with open(SETTINGS_FILE, "w") as outfile:
        json.dump(settings, outfile ,indent=4) 

def load_settings_from_json():
    ''' Read the encryption Key from the settings.json file'''

    with open(SETTINGS_FILE) as infile:
        settings=json.load(infile)
    return settings


def initialize_encryption():
    '''Initialize Encryption Key by generating random password'''
    
    iv = secrets.randbits(256)
    key=create_encryption_key(random_password_generator())
    create_settings_json(key,iv)


def main():

    settings = load_settings_from_json()
    my_key = decode_key_from_json(settings[JSON_KEY_KEY])
    iv2 = settings[JSON_KEY_IV]

    plaintext = "The random Text for encryption"
    ciphertext=encrypt(plaintext,my_key,iv2)

    decrypted = decrypt(ciphertext,my_key,iv2)
    print('Decrypted:', decrypted)


def random_password_generator():
    lower="abcdefghijklmnopqrstuvwxyz"
    upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers="1234567890"
    symbols="!@#$&_"
    all=lower+upper+numbers+symbols
    password_length=14
    password= "".join(random.sample(all,password_length))
    return password

if __name__=="__main__":
    main()