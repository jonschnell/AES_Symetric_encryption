'''
Created on Jan 7, 2020

@author: Jonathon Schnell

@date: 1/10/2019

@version: 1.0

'''

import argparse
import sys
import os
from getpass import getpass
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


if __name__ == '__main__':
    #argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", default='false', help="[key.key] to be used")
    parser.add_argument("-e", "--encrypt", default='false', help="[file.txt] to be encrypted")
    parser.add_argument("-d", "--decrypt", default='false', help="[file.txt] to be decrypted")
    parser.add_argument("-f", "--file", nargs="?", default='false', help="saves decrypted or encrypted data to [filename.txt]")
    parser.add_argument("-g", "--keyGen", default='false', help="generate key [filename.key]")


    args = parser.parse_args()
    
    key = args.key
    
    
    #encrypt data with fernet
    def encryptMessage(message, key):
        #create fernet object with key
        f = Fernet(key)
        
        #encode message
        encoded = message.encode()
    
        #encrypt the message
        token = f.encrypt(encoded)
        
        return token
    
    #decrypt data with fernet
    def decryptMessage(token, key):
        #create fernet object with key
        f = Fernet(key)
        
        #decrypt the message
        message = f.decrypt(token)
        
        return message
    
    #write and encrypted message to file
    def writeEncrypt():
        f = open(args.file, "wb")
        f.write(encryptMessage(string, key))
        f.close
        print(args.file + " created")
        
    #write and decrypted message to file
    def writeDecrypt():
        f = open(args.file, "wb")
        f.write(decryptMessage(string, key))
        f.close
        print(args.file + " created")
        
    #ensure file exists
    def fileCheck(fn):
        try:
            open(fn, "r")
            return 1
        except IOError:
            sys.exit("Error: File does not appear to exist.")
            

   
    if args.keyGen != "false":
        keyfile = args.keyGen
        print("Randomly generated keys will not have an associated password and salt\nSelecting no will require you to enter a password and allow you to generate a new salt\nor use your own salt.salt\nWould you like a randomly generated key? (y/n)")
        x = raw_input()
        if x == 'y':
            key = Fernet.generate_key()
            f = open(keyfile, "wb")
            f.write(key)
            f.close
            print(keyfile + " generated")
        else:
            print("would you like to generate a new salt?")
            y = raw_input()
            if y == 'y':
                print("what would you like the name of your salt file to be? (include extension such as .salt)")
                newsaltfile = raw_input()
                salt = os.urandom(16)
                f = open(newsaltfile, "wb")
                f.write(salt)
                f.close()
                print(newsaltfile + " created")
            print("enter the name of the salt.salt you would like to use for a new key")
            
            saltfile = raw_input()
            fileCheck(saltfile)
            
            print("enter the password for the new key.")
            password = getpass()
            passwordencoded = password.encode()
            #salt = b'\xda\xcd`\x91\xab\x00\xac\xde\x9b\x9f\x08\xb3\xf0\xb7\xedT'
            f = open(saltfile, "rb")
            salt = f.read()
            f.close()
            #key derivation function
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
                )

            key = base64.urlsafe_b64encode(kdf.derive(passwordencoded))
            print (key)
            
            f = open(keyfile, "wb")
            f.write(key)
            f.close
   
    
    #-e set
    elif args.encrypt != "false":
        
        fileCheck(key)
        f = open(key, 'rb')
        key = f.read()
        f.close()
        
        enc = args.encrypt
        fileCheck(enc)
        f = open(enc, "rb")
        string = f.read()
        f.close
        print(encryptMessage(string, key))
        #-f set
        if args.file != "false":
            writeEncrypt()
    #-d set
    elif args.decrypt != "false":
        
        fileCheck(key)
        f = open(key, 'rb')
        key = f.read()
        f.close()
        
        dec = args.decrypt
        fileCheck(dec)
        f = open(dec, "rb")
        string = f.read()
        f.close
        print(decryptMessage(string, key))
        #-f set
        if args.file != "false":
            writeDecrypt()


    
        #base case
    else:
        print("please use either -e [file.txt] or -d [file.txt] to encrypt or decrypt the data")
