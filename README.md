# AES_Symmetric_encryption
This python script allows you to generate salts and keys then use those keys to encrypt and decrypt files.

To use this program you will need the python cryptography package
`sudo python -m pip install`
from there you will need a salt and a key to encrypt and decrypt files

to generate a key and salt
`python AES.py -g [keyfile.key]`
from there follow the step by step key and salt generation process
```Randomly generated keys will not have an associated password and salt
Selecting no will require you to enter a password and allow you to generate a new salt
or use your own salt.salt
Would you like a randomly generated key? (y/n)
>n
would you like to generate a new salt?
>y
what would you like the name of your salt file to be? (include extension such as .salt)
>exampleSalt.salt
exampleSalt.salt created
enter the name of the salt.salt you would like to use for a new key
>exampleSalt.salt
enter the password for the new key.
Password:**********
WjF7O0dX899g8dvtJNZmkH5yS1Jm5w3IEpryKWnvAek=
key.key created
```

To encrypt files
`python AES.py -k [key.key] -e [file]`

to decrypt files
`python AES.py -k [key.key] -d [file]`

It should be noted that the file name following the -e anf -d flags do not need to be present. In they case that they are not present the data will just be printed to the command line.
