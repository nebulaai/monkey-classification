import tensorflow as tf
from tensorflow.python.client import device_lib
print(tf.__version__)
# print("Num of GPUs available: ", len(tf.test.gpu_device_name()))

print(device_lib.list_local_devices())
