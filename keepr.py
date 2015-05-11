from binascii import hexlify
from getpass import getpass
from sys import stdin, argv
import sys 
from simplecrypt import encrypt, decrypt

try:
    script, filename, option = argv
except Exception as error:
    print("usage: python keepr.py FILENAME OPTION")
    print("options: ")
    print("\t -r read from filename")
    print("\t -w write to filename")
    print("\t -a append to filename on newline")
    print("example: python keepr.py mysecret.txt -r")
    sys.exit()
    
if option == '-w':
    print("This will overwrite "+str(filename)+"! Press CTRL-C to abort.")

    # read the password from the user (without displaying it)
    password = getpass("password: ")
    password2 = getpass("again: ")
    if password != password2:
        print("error: passwords don't match! aborting!")
        sys.exit()

    # read the plaintext we will encrypt
    print("enter EOF on a line when finished")
    print("message: ")
    text = ""
    stopword = "EOF"
    for line in iter(input, stopword):
        text += line+'\n'
        
    message = text
    
    # encrypt the plaintext.  we explicitly convert to bytes first (optional)
    ciphertext = encrypt(password, message.encode('utf8'))
    
    text_file = open(filename, 'wb')
    text_file.write(ciphertext)
    text_file.close()

    # the ciphertext plaintext is bytes, so we display it as a hex string
    print("ciphertext: %s" % hexlify(ciphertext))

    # now decrypt the plaintext (using the same salt and password)
    plaintext = decrypt(password, ciphertext)

    # the decrypted plaintext is bytes, but we can convert it back to a string
    print("plaintext: %s" % plaintext)
    print("plaintext as string:\n%s" % plaintext.decode('utf8'))
    print("ciphertext saved to "+str(filename))
    
elif option == '-r':
    print("enter password for "+str(filename))
    password = getpass("password: ")

    ciphertext = bytearray()
    
    with open(filename, "rb") as f:
        byte = f.read(1)
        while byte:
            ciphertext += byte
            byte = f.read(1)

    plaintext = decrypt(password, bytes(ciphertext))
        
    print("plaintext: %s" % plaintext)
    print("plaintext as string:\n%s" % plaintext.decode('utf8'))

elif option == '-a':
    # read the existing text
    print("enter password for "+str(filename))    
    password = getpass("password: ")

    ciphertext = bytearray()
    
    with open(filename, "rb") as f:
        byte = f.read(1)
        while byte:
            ciphertext += byte
            byte = f.read(1)

    existing_plaintext = decrypt(password, bytes(ciphertext))
        
    # read the plaintext we will encrypt and append
    print("enter EOF on a line when finished")
    print("message: ")
    text = ""
    stopword = "EOF"
    for line in iter(input, stopword):
        text += line+'\n'

    # new message consisting of existing_plaintext and new text
    message = existing_plaintext.decode('utf8')+text
   
    # encrypt the plaintext.  we explicitly convert to bytes first (optional)
    ciphertext = encrypt(password, message.encode('utf8'))
    
    text_file = open(filename, 'wb')
    text_file.write(ciphertext)
    text_file.close()

    # the ciphertext plaintext is bytes, so we display it as a hex string
    print("ciphertext: %s" % hexlify(ciphertext))

    # now decrypt the plaintext (using the same salt and password)
    plaintext = decrypt(password, ciphertext)

    # the decrypted plaintext is bytes, but we can convert it back to a string
    print("plaintext: %s" % plaintext)
    print("plaintext as string:\n%s" % plaintext.decode('utf8'))
    print("ciphertext saved to "+str(filename))

else:    
    print("usage: python keepr.py FILENAME OPTION")
    print("options: ")
    print("\t -r read from filename")
    print("\t -w write to filename")
    print("\t -a append to filename on newline")
    print("example: python keepr.py mysecret.txt -r")
    sys.exit()
    
