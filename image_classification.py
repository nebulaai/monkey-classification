import tensorflow as tf
from datetime import datetime

print(tf.__version__)
print("Num of GPUs available: ", len(tf.test.gpu_device_name()))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os


from keras.api._v2.keras.applications.resnet50 import ResNet50
from keras.api._v2.keras.preprocessing.image import ImageDataGenerator
from keras.api._v2.keras.applications.resnet50 import preprocess_input
from keras.api._v2.keras.optimizers import Adam
def image_classification(dataset_path, training_data, validation_data):
    isdir = os.path.isdir(dataset_path)
    if isdir:
        print("Dataset Monkey found.")

    # load training and testing sets
    train_dataset_path = dataset_path + training_data
    test_dataset_path = dataset_path + validation_data
    datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    train = datagen.flow_from_directory(train_dataset_path, target_size=(160, 160), batch_size=32)
    test = datagen.flow_from_directory(test_dataset_path, target_size=(160, 160), batch_size=32, shuffle=False)

    # read labels
    file = pd.read_csv(dataset_path +'monkey_labels.txt', sep='[\s,]{2,20}', engine='python')
    labels = file['Common Name']
    labels

    # display images of each category
    print(train_dataset_path)
    folders = os.listdir(train_dataset_path)
    folders.sort()
    print(folders)
    for i, folder in enumerate(folders):
        path = train_dataset_path + '/' + folder
        imgs = os.listdir(path)
        plt.figure(figsize=(20, 3))
        for j in range(5):
            img = cv2.cvtColor(cv2.imread(path + '/' + imgs[j]), cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (640, 640))
            plt.subplot(1, 5, j + 1)
            plt.imshow(img)
            plt.axis('off')
        plt.suptitle(labels[i], fontsize="20")
        print("\n\n")

    IMG_SHAPE = (160, 160, 3)
    base_model = ResNet50(include_top=False, weights='imagenet', input_shape=IMG_SHAPE)

    base_model.trainable = False
    inputs = tf.keras.Input(shape=IMG_SHAPE)
    x = base_model(inputs, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(1024, activation='relu')(x)
    x = tf.keras.layers.Dense(514, activation='relu')(x)
    outputs = tf.keras.layers.Dense(10, activation='softmax')(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)

    model.summary()

    model.compile(optimizer=Adam(lr=0.0001),
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    history = model.fit(train, epochs=5)

    print(history.history)
    acc = history.history['accuracy']
    loss = history.history['loss']

    plt.figure(figsize=(8, 8))
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Training Accuracy')
    plt.legend(loc='lower right')
    plt.ylabel('Accuracy')
    plt.title('Training Accuracy')

    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Training Loss')
    plt.legend(loc='upper right')
    plt.ylabel('Cross Entropy')
    plt.title('Training Loss')
    plt.xlabel('epoch')

    prediction = model.predict_generator(test)
    predicted_classes = np.argmax(prediction, axis=1)
    test_acc = np.mean(predicted_classes == test.classes)
    print("Test accuracy: {:.6f}".format(test_acc))

    show_test = ImageDataGenerator().flow_from_directory(test_dataset_path, target_size=(160, 160), batch_size=test.samples,
                                                        shuffle=False)
    x, _ = show_test.next()
    classes = test.classes

    # generate random indices
    random_indices = np.random.randint(0, test.samples, size=28)

    # prediction
    plt.figure(figsize=(20, 30))
    for i, idx in enumerate(random_indices):
        img = np.uint8(x[idx])
        plt.subplot(7, 4, i + 1)
        plt.imshow(img)
        plt.axis('off')
        plt.title("class: " + labels[classes[idx]] + "\npredicted: " + labels[predicted_classes[idx]])
    plt.savefig(dataset_path + '/result.png')

    print("Completed at ", datetime.now())