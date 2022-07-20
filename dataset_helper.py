import os
import sys
import zipfile
import requests
import os
import random
import struct

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from sklearn.metrics import classification_report

from mcs.contract import ContractAPI
from mcs.api import McsAPI

from image_classification import image_classification

wallet_info = {
        'wallet_address' : '',
        'private_key' : '',
        'web3_api' : '',
    }

def data_fetch(ipfs_uri, dataset_path, file_name, dir_name, extract=False):

    isdir = os.path.isdir(dataset_path)
    if isdir:
        print("Dataset found on local drive: ", dataset_path)
    else:
        print("Start downloading dataset")
        link = ipfs_uri

        os.mkdir(dir_name)

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
        if extract:
           file_extract(file_name, dir_name)

def file_extract(file_name, dir_name):
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall(dir_name)   

def upload_to_mcs(wallet_address, private_key, web3_api, file_path):
    # upload to mcs
    w3_api = ContractAPI(web3_api)
    api = McsAPI()

    w3_api.approve_usdc(wallet_address, private_key, "1")
    # upload file to mcs
    father_path = os.path.abspath(os.path.dirname(__file__))
    print(father_path+file_path)
    upload_file = api.upload_file(wallet_address, father_path + file_path)
    file_data = upload_file["data"]
    payload_cid, source_file_upload_id, nft_uri, file_size, w_cid = file_data['payload_cid'], file_data[
        'source_file_upload_id'], file_data['ipfs_url'], file_data['file_size'], file_data['w_cid']
    # get the global variable
    params = api.get_params()["data"]
    # get filcoin price
    rate = api.get_price_rate()["data"]
    # test upload_file_pay contract
    w3_api.upload_file_pay(wallet_address, private_key, file_size, w_cid, rate, params)
    print('finished upload')
    return payload_cid, source_file_upload_id

def get_payment_info(wallet_address, payload_cid, source_file_upload_id):
    api = McsAPI()
    # get task information from mcs
    payment_info = api.get_payment_info(payload_cid, wallet_address, source_file_upload_id)
    return payment_info

def get_mcs_url(wallet_address, source_file_upload_id):
    api = McsAPI()
    deal_detail = api.get_deal_detail(wallet_address, source_file_upload_id)
    download_url = deal_detail["data"]["source_file_upload_deal"]["ipfs_url"]
    return download_url

def encrypt_file(key, filename, chunk_size=64 * 1024):
    print("Data %s encryption starts " % filename)
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


def decrypt_file(key, filename, chunk_size=24 * 1024):
    print("Data %s decryption starts " % filename)
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


if __name__ == "__main__":
    # download data from data source
    ipfs_monkey_cid = "https://calibration-ipfs.filswan.com/ipfs/QmWuHREwKXLbBRV94zxmgG3qP7EADUDuyQ3jAYazC5Pd8c"
    data_fetch(ipfs_monkey_cid, dataset_path="./dataset/monkeys", file_name="dataset/monkeys.zip", dir_name="dataset", extract=True)
    # Encrypt file:
    if not os.path.isdir('key.txt'):
        f = open("key.txt", "wb")
        f.write(get_random_bytes(32))
        f.close()

    # create an data encryption key
    f = open("key.txt", "rb")
    key = f.read()

    # encrypt_file
    encrypt_file(key, './dataset/monkeys.zip')

    # Set up wallet info
    wallet_address = wallet_info['wallet_address']
    private_key = wallet_info['private_key']
    web3_api = wallet_info['web3_api']

    # upload to mcs
    filepath = '/dataset/monkeys.zip.encrypted'
    payload_cid, source_file_upload_id = upload_to_mcs(wallet_address, private_key, web3_api, filepath)
    print(get_payment_info(wallet_address, payload_cid, source_file_upload_id))

    # get sps from MCS
    download_url = get_mcs_url(wallet_address, source_file_upload_id)
    print(download_url)

    # download data from mcs ipfs for machine learning
    data_fetch(download_url, dataset_path="./download/monkeys", file_name="download/monkeys.zip.encrypted", dir_name="download")
    # * decrypt_file
    decrypt_file(key, filename="./download/monkeys.zip.encrypted")
    os.rename(src='download/monkeys.zip.encrypted.decrypted', dst='download/monkeys.zip')
    file_extract('download/monkeys.zip', 'download')
    # * ML
    image_classification(dataset_path="./download/monkeys/", training_data='training/training', validation_data='validation/validation')
    # upload training result to mcs
    
    payload_cid, source_file_upload_id = upload_to_mcs(wallet_address, private_key, web3_api, './download/monkeys/result.png')
    download_url = get_mcs_url(wallet_address, source_file_upload_id)
    print(download_url)
