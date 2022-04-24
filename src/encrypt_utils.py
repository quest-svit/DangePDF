#!/usr/bin/python env

import base64
import json
import random
import pyaes, pbkdf2, binascii, os, secrets
import os.path,platform
import logging_handler

ENCODING_UTF_8='utf-8'
JSON_KEY_KEY = "key"
JSON_KEY_IV = "iv"
CONFIG_FOLDER_NAME='/.dange-pdf'
FILE_PROTOCOL="file://"
SETTINGS_FILE_NAME = "/settings.json"
log=logging_handler.create_logging_handler()



if (platform.system() == 'Linux' or platform.system() == 'Darwin'):
    if not os.path.exists(os.path.expanduser('~')+ CONFIG_FOLDER_NAME):
        os.makedirs(os.path.expanduser('~')+ CONFIG_FOLDER_NAME)
    SETTINGS_FILE=os.path.expanduser('~')+ CONFIG_FOLDER_NAME + SETTINGS_FILE_NAME
elif platform.system() == 'Windows':
    if not os.path.exists(os.path.expandvars(R"% HOMEPATH %")+ CONFIG_FOLDER_NAME):
        os.makedirs(os.path.expandvars(R"% HOMEPATH %")+ CONFIG_FOLDER_NAME)
    SETTINGS_FILE=os.path.expandvars(R"% HOMEPATH %")+ CONFIG_FOLDER_NAME + SETTINGS_FILE_NAME
else:
    pass



class EncryptUtils(object):

    def __init__(self):
        log.debug(SETTINGS_FILE)
        if os.path.exists(SETTINGS_FILE):
            log.info("Loading settings.json")
            settings = self.load_settings_from_json()
            self.key = self.decode_key_from_json(settings[JSON_KEY_KEY])
            self.iv=settings[JSON_KEY_IV]
        else:
            log.info("Settings.json doesn't exist. Initializing Encryption.")
            self.initialize_encryption()

    def create_encryption_key(self,password):
        ''' Derive a 256-bit AES encryption key from the password '''

        SALT_LENGTH = 32
        passwordSalt = os.urandom(SALT_LENGTH)
        key = pbkdf2.PBKDF2(password, passwordSalt).read(SALT_LENGTH)
        return key

    def random_password_generator():
        lower="abcdefghijklmnopqrstuvwxyz"
        upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers="1234567890"
        symbols="!@#$&_"
        all=lower+upper+numbers+symbols
        password_length=14
        password= "".join(random.sample(all,password_length))
        return password
    
    def random_filename_generator():
        lower="abcdefghijklmnopqrstuvwxyz"
        upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        all=lower+upper
        filename_length=14
        filename= "".join(random.sample(all,filename_length))
        return filename

    def initialize_encryption(self):
            '''Initialize Encryption Key by generating random password'''
            
            self.iv = secrets.randbits(256)
            self.key=self.create_encryption_key(EncryptUtils.random_password_generator())
            self.create_settings_json()


    def encrypt(self, plaintext):
        ''' Encrypt the plaintext with the given key'''

        aes = pyaes.AESModeOfOperationCTR(self.key, pyaes.Counter(self.iv))
        return aes.encrypt(plaintext)


    def decrypt(self, ciphertext):
        ''' Decrypt the ciphertext with the given key '''

        aes = pyaes.AESModeOfOperationCTR(self.key, pyaes.Counter(self.iv))
        return aes.decrypt(ciphertext)

    def encode_for_json_compatibility(self):
        '''JSON only supports UTF-8 characters where as the KEY generated is a bytes data-type
        Hence we need to convert to UTF-8 for storing in JSON'''

        return binascii.hexlify(self.key).decode(ENCODING_UTF_8)

    def decode_key_from_json(self, json_key_value):
        '''JSON only supports UTF-8 characters where as the KEY generated is a bytes data-type
        Hence we need to convert back to bytes for decryption'''

        return binascii.unhexlify(json_key_value.encode(ENCODING_UTF_8))

    def create_settings_json(self):
        ''' Create the settings.json file to store encryption Key'''

        settings = {}
        settings[JSON_KEY_KEY]= self.encode_for_json_compatibility()
        settings[JSON_KEY_IV]= self.iv

        log.info(SETTINGS_FILE)
        with open(SETTINGS_FILE, "w") as outfile:
            json.dump(settings, outfile ,indent=4) 

    def load_settings_from_json(self):
        ''' Read the encryption Key from the settings.json file'''

        with open(SETTINGS_FILE) as infile:
            settings=json.load(infile)
        return settings


    

def test_encrypt_utils():

    encrypt_util=EncryptUtils()

    plaintext = "The random Text for encryption"
    ciphertext=encrypt_util.encrypt(plaintext)

    decrypted = encrypt_util.decrypt(ciphertext)
    log.info('Decrypted:', decrypted)


  

if __name__=="__main__":
    test_encrypt_utils()