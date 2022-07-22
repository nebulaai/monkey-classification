# Image Classification


## Dataset

10 Monkey Species: https://www.kaggle.com/slothkong/10-monkey-species

### Install Lib

Install open cv

```
pip install opencv
```

Install Python lib

```
pip install matplotlib
pip install pillow
pip install scipy
```

Install TensorFlow

```
pip install opencv-contrib-python==4.5.5.64
pip install --upgrade TensorFlow

```

## Running dataset helper

```
python dataset_helper.py
```

Download monkeys data (https://calibration-ipfs.filswan.com/ipfs/QmWuHREwKXLbBRV94zxmgG3qP7EADUDuyQ3jAYazC5Pd8c) \

Fetch and extract training and valiadation data. \

Encrypt data

```python
encrypt_file(key, './dataset/monkeys.zip')
```

Upload to mcs \

```python
payload_cid, source_file_upload_id = upload_to_mcs(wallet_address, private_key, web3_api, filepath)
```

Get file mcs url

```python
deal_detail = api.get_deal_detail(wallet_address, source_file_upload_id)
download_url = deal_detail["data"]["source_file_upload_deal"]["ipfs_url"]
```

Run ML algorithm

```
image_classification(dataset_path="./download/monkeys/", training_data='training/training', validation_data='validation/validation')
```