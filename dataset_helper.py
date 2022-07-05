import os
import sys
import zipfile
import requests
import os
import random
import struct

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

ipfs_monkey_cid = "https://calibration-ipfs.filswan.com/ipfs/QmWuHREwKXLbBRV94zxmgG3qP7EADUDuyQ3jAYazC5Pd8c"


def data_fetch(ipfs_uri):
    dataset_path = "./dataset/monkeys"
    file_name = "dataset/monkeys.zip"

    isdir = os.path.isdir(dataset_path)
    if isdir:
        print("Dataset Monkey found on local drive: ", dataset_path)
    else:
        print("Start downloading dataset")
        link = ipfs_uri

        with open(file_name, "wb") as f:
            print("Downloading %s" % file_name)
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall("./dataset")


def decrypt_file(key, filename, chunk_size=24 * 1024):
    input_file = open(filename, 'rb')
    output_file = open(filename + '.decrypted', 'wb')
    buffer_size = 65536  # 64kb

    iv = input_file.read(16)

    cipher_encrypt = AES.new(key, AES.MODE_CFB, iv=iv)

    buffer = input_file.read(buffer_size)
    while len(buffer) > 0:
        decrypted_bytes = cipher_encrypt.decrypt(buffer)
        output_file.write(decrypted_bytes)
        buffer = input_file.read(buffer_size)

    input_file.close()
    output_file.close()
    print("Data %s decrypted" % filename)


def encrypt_file(key, filename, chunk_size=64 * 1024):
    file_to_encrypt = filename
    buffer_size = 65536  # 64kb

    input_file = open(file_to_encrypt, 'rb')
    output_file = open(file_to_encrypt + '.encrypted', 'wb')

    cipher_encrypt = AES.new(key, AES.MODE_CFB)

    output_file.write(cipher_encrypt.iv)

    buffer = input_file.read(buffer_size)
    while len(buffer) > 0:
        ciphered_bytes = cipher_encrypt.encrypt(buffer)
        output_file.write(ciphered_bytes)
        buffer = input_file.read(buffer_size)

    input_file.close()
    output_file.close()
    print("Data %s encrypted: %s " % (filename, file_to_encrypt + '.encrypted'))


# Encrypt file:
key = get_random_bytes(32)
encrypt_file(key, './dataset/monkeys.zip')

# Decrypt file:
decrypt_file(key, './dataset/monkeys.zip.encrypted')
##
# Example usage:
##
data_fetch(ipfs_monkey_cid)
