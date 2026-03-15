import numpy as np

from pathlib import Path
import os
import matplotlib.pyplot as plt
import time
import cv2 as cv


import datetime
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.utils import to_categorical
import glob
from tensorflow import keras
from tensorflow.keras import layers

w = [1, 0, 0, 0, 0, 0, 0, 0, 0]
s = [0, 1, 0, 0, 0, 0, 0, 0, 0]
a = [0, 0, 1, 0, 0, 0, 0, 0, 0]
d = [0, 0, 0, 1, 0, 0, 0, 0, 0]
wa = [0, 0, 0, 0, 1, 0, 0, 0, 0]
wd = [0, 0, 0, 0, 0, 1, 0, 0, 0]
sa = [0, 0, 0, 0, 0, 0, 1, 0, 0]
sd = [0, 0, 0, 0, 0, 0, 0, 1, 0]
nk = [0, 0, 0, 0, 0, 0, 0, 0, 1]


def convertToArrows(directions):
    # convert [0 1 0 0 0 0 0 0 0] to [0, 1, 0, 0, 0, 0, 0, 0, 0]
    directions = directions.tolist()
    if directions == w:
        return '↑'
    elif directions == s:
        return '↓'
    elif directions == a:
        return '←'
    elif directions == d:
        return '→'
    elif directions == wa:
        return '↖'
    elif directions == wd:
        return '↗'
    elif directions == sa:
        return '↙'
    elif directions == sd:
        return '↘'
    elif directions == nk:
        return 'NOKEY'


class TrainingModel():

    def __init__(self):
        pass

    def clean_data(self, fileName, merge=False):
        # CLEAN DATA
        print("CLEAN DATA")
        starting_value = 1
        training_data = []
        while True:
            file_name = './data/' + fileName + '/' + \
                fileName + '-{}.npy'.format(starting_value)

            if os.path.isfile(file_name):
                training_data_tmp = np.load(file_name, allow_pickle=True)
                print('training_data_tmp: ', len(training_data_tmp))
                # add training_data_tmp to training_data
                for data in training_data_tmp:
                    training_data.append(data)
                print('training_data: ', len(training_data))
                starting_value += 1
            else:
                break

        print('training_data before: ', len(training_data))

        if merge is False:

            unique_data = {}

            for data in training_data:
                img = data[0]
                choice = data[1]

                # calculate unique hash for img + choice
                hash_value = hash(str(img.tolist()) + str(choice))

                # check if hash_value is already in unique_data
                if hash_value in unique_data:
                    # compare img and choice with those already in unique_data
                    for other_data in unique_data[hash_value]:
                        if np.array_equal(img, other_data[0]) and np.array_equal(choice, other_data[1]):
                            # if img + choice is equal to another img + choice, then don't add to unique_data
                            break
                    else:
                        # if img + choice is not equal to any other img + choice with same hash, then add to unique_data
                        unique_data[hash_value].append(data)
                else:
                    # if hash_value is not in unique_data, then add to unique_data
                    unique_data[hash_value] = [data]

            # convert unique_data back to a list of tuples
            training_data = [(data[0], data[1])
                            for data_list in unique_data.values() for data in data_list]

            print('training_data after: ', len(training_data))
        
        else:
            # convert unique_data back to a list of tuples
            # training_data = [(data[0], data[1])
            #                 for data_list in training_data for data in data_list]

            print('training_data after: ', len(training_data))

        training_data = np.array(training_data, dtype=object)

        # create folder if not exists
        if not os.path.exists('./data/' + fileName + '_clean'):
            os.makedirs('./data/' + fileName + '_clean')
        np.save('./data/' + fileName + '_clean' + '/' +
                fileName + '_clean-1', training_data)
        training_data = []
        # CLEAN DATA
        print("CLEAN DATA DONE")

    def prepare_training_data(self, FILE_NAME, imageGen=False):

        # carga los datos
        data = np.load('./data/{}/{}-1.npy'.format(FILE_NAME,
                       FILE_NAME), allow_pickle=True)

        # Separar las imágenes y etiquetas
        x = data[:, 0]
        y = data[:, 1]

        # Convertir las imágenes a un array numpy
        x = np.array([i for i in x]).reshape(-1, 110, 173, 1)

        # convertir las etiquetas a un array numpy dtype=uint8
        y = np.array([i for i in y])

        print(x.shape)

        if imageGen:
            # aumentar las imágenes
            datagen = ImageDataGenerator(
                rotation_range=20,
                width_shift_range=0.2,
                height_shift_range=0.2,
                zoom_range=0.2,
                horizontal_flip=False,
                vertical_flip=False,
                fill_mode='nearest')

            # crear un generador de imágenes
            datagen.fit(x)

            # generar las imágenes aumentadas
            batch_size = 1
            data_generator = datagen.flow(
                x, batch_size=batch_size, shuffle=False)

            # recorrer el generador y agregar los lotes a una lista
            augmented_data = []
            steps_per_epoch = int(np.ceil(len(x) / batch_size))
            for i in range(steps_per_epoch):
                batch = data_generator.next()
                augmented_data.append(batch[0])

            # convertir la lista en un array numpy
            x = np.array(augmented_data).reshape(-1, 110, 173, 1)

        # Separar los datos en un conjunto de entrenamiento y validación
        x_train_val, y_train_val = x, y
        x_train, x_validate, y_train, y_validate = train_test_split(
            x_train_val, y_train_val, test_size=0.1, random_state=42)

        x_train = x_train / 255.0
        x_validate = x_validate / 255.0

        # mezclar los datos
        indices = np.arange(len(x_train))
        np.random.shuffle(indices)
        x_train = x_train[indices]
        y_train = y_train[indices]

        # plt.figure(figsize=(10,10))
        # for i in range(100):
        #     plt.subplot(10,10,i+1)
        #     plt.xticks([])
        #     plt.yticks([])
        #     plt.grid(False)
        #     plt.imshow(x_train[i].reshape(110, 173), cmap=plt.cm.binary)
        #     plt.xlabel(convertToArrows(y_train[i]))
        # plt.show()

        print('len(x_train): ', len(x_train))
        print('len(y_train): ', len(y_train))
        print('len(x_validate): ', len(x_validate))
        print('len(y_validate): ', len(y_validate))

        return (x_train, y_train), (x_validate, y_validate)

    def prepare_model(self, typeOfModel):
        # check if model exists
        # model_files = glob.glob("./models/*typeOfModel__model-*")
        # if len(model_files) > 0:
        #     print('Model exists, loading previous model ')
        #     with tf.device('/GPU:0'): # especificar la GPU
        #         # get the modern file
        #         best_model_path = max(model_files, key=os.path.getctime)
        #         model = keras.models.load_model(best_model_path, compile=False)
        #         # get the last epoch from the best model
        #         print (best_model_path)
        #         last_epoch = int(best_model_path.split('__model-')[1].split('-')[0])
        #         EPOCHS = int(last_epoch) + EPOCHS
        #     print('Model ' + best_model_path + ' loaded!')
        # else:

        if typeOfModel == 'modelv1' or typeOfModel == 'modelv1_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv2' or typeOfModel == 'modelv2_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Flatten(input_shape=(110, 173, 1)),
                    tf.keras.layers.Dense(150, activation='relu'),
                    tf.keras.layers.Dense(150, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv3' or typeOfModel == 'modelv3_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(100, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        

        if typeOfModel == 'modelv5' or typeOfModel == 'modelv5_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(256, activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv6' or typeOfModel == 'modelv6_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        64, (3, 3), activation='relu', padding='same', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Conv2D(
                        128, (3, 3), activation='relu', padding='same'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Conv2D(
                        256, (3, 3), activation='relu', padding='same'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(256, activation='relu'),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv7' or typeOfModel == 'modelv7_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv8' or typeOfModel == 'modelv8_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(512, activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Dense(256, activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv9' or typeOfModel == 'modelv9_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv10' or typeOfModel == 'modelv10_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(256, activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv11' or typeOfModel == 'modelv11_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(512, activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Dense(256, activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        

        if typeOfModel == 'modelv13' or typeOfModel == 'modelv13_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.models.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv14' or typeOfModel == 'modelv14_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.models.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(500, activation='relu'),
                    tf.keras.layers.Dense(500, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        

        if typeOfModel == 'modelv16' or typeOfModel == 'modelv16_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.models.Sequential([
                    tf.keras.layers.Conv2D(
                        64, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(512, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    # aumentamos el factor de dropout
                    tf.keras.layers.Dropout(0.7),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv17' or typeOfModel == 'modelv17_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.models.Sequential([
                    tf.keras.layers.Conv2D(
                        64, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    # aumentamos el factor de dropout
                    tf.keras.layers.Dropout(0.7),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv18' or typeOfModel == 'modelv18_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.models.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.7),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(255, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv19' or typeOfModel == 'modelv19_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.models.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.3),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv20' or typeOfModel == 'modelv20_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.models.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv21' or typeOfModel == 'modelv21_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.models.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.9),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv4' or typeOfModel == 'modelv4_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv12' or typeOfModel == 'modelv12_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        64, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv23' or typeOfModel == 'modelv23_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        64, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.7),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv15' or typeOfModel == 'modelv15_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.models.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.7),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv24' or typeOfModel == 'modelv24_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        16, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv25' or typeOfModel == 'modelv25_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        8, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(16, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv29' or typeOfModel == 'modelv29_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv30' or typeOfModel == 'modelv30_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Conv2D(192, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv28' or typeOfModel == 'modelv28_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.7),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv31' or typeOfModel == 'modelv31_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Conv2D(192, (3, 3), activation='relu'),
                    tf.keras.layers.BatchNormalization(),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv32' or typeOfModel == 'modelv32_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv33' or typeOfModel == 'modelv33_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv34' or typeOfModel == 'modelv34_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(150, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv27' or typeOfModel == 'modelv27_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv36' or typeOfModel == 'modelv36_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(350, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv22' or typeOfModel == 'modelv22_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv35' or typeOfModel == 'modelv35_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.1),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv38' or typeOfModel == 'modelv38_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.1),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv39' or typeOfModel == 'modelv39_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.1),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.7),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv40' or typeOfModel == 'modelv40_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.1),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv37' or typeOfModel == 'modelv37_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.1),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.1),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv41' or typeOfModel == 'modelv41_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv42' or typeOfModel == 'modelv42_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.85),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv43' or typeOfModel == 'modelv43_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.90),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv44' or typeOfModel == 'modelv44_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(255, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv45' or typeOfModel == 'modelv45_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(260, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv46' or typeOfModel == 'modelv46_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(265, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv47' or typeOfModel == 'modelv47_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(245, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv48' or typeOfModel == 'modelv48_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(240, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

                # ----------------------------------
                # ----------------------------------
                # ----------------------------------
                # ----------------------------------
                # ----------------------------------
                # ----------------------------------
        
        if typeOfModel == 'modelv26' or typeOfModel == 'modelv26_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.8),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        
        if typeOfModel == 'modelv49' or typeOfModel == 'modelv49_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv50' or typeOfModel == 'modelv50_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.6),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv51' or typeOfModel == 'modelv51_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.7),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv52' or typeOfModel == 'modelv52_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.3),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(250, activation='relu'),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
                
        if typeOfModel == 'modelv53' or typeOfModel == 'modelv53_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                    # |Best Value So Far |Hyperparameter
                    # |0.2               |drop_rate
                    # |64                |input_units
                    # |2                 |n_layers
                    # |32                |conv_0_units
                    # |96                |dense_0_units
                    # |adam              |optimizer
                    # |categorical_cro...|loss
                    # |32                |conv_1_units
                    # |32                |dense_1_units
                    # |None              |conv_2_units
                    # |None              |dense_2_units
                    # |None              |conv_3_units
                    # |None              |dense_3_units

                    tf.keras.layers.Conv2D(
                        64, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(96, activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.Dense(32, activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])

        if typeOfModel == 'modelv54' or typeOfModel == 'modelv54_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                # Best Value So Far |Hyperparameter
                # 0                 |drop_rate
                # 128               |input_units
                # 3                 |n_layers
                # 96                |conv_0_units
                # 224               |dense_0_units
                # adam              |optimizer
                # categorical_cro...|loss
                # 64                |conv_1_units
                # 128               |conv_2_units
                # 128               |conv_3_units
                # 64                |dense_1_units
                # 224               |dense_2_units
                # 128               |dense_3_unit

                    tf.keras.layers.Conv2D(
                        128, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0),
                    tf.keras.layers.Conv2D(96, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0),
                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(224, activation='relu'),
                    tf.keras.layers.Dropout(0),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.Dropout(0),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv55' or typeOfModel == 'modelv55_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential([
                #Best Value So Far |Hyperparameter
                #0                 |drop_rate
                #32                |input_units
                #3                 |n_layers
                #192               |conv_0_units
                #128               |dense_0_units
                #adam              |optimizer
                #categorical_cro...|loss
                #224               |conv_1_units
                #128               |conv_2_units
                #160               |conv_3_units
                #96                |dense_1_units
                #32                |dense_2_units
                #192               |dense_3_units

                    tf.keras.layers.Conv2D(
                        32, (3, 3), activation='relu', input_shape=(110, 173, 1)),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0),
                    tf.keras.layers.Conv2D(192, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0),
                    tf.keras.layers.Conv2D(224, (3, 3), activation='relu'),
                    tf.keras.layers.MaxPooling2D((2, 2)),
                    tf.keras.layers.Dropout(0),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.Dropout(0),
                    tf.keras.layers.Dense(96, activation='relu'),
                    tf.keras.layers.Dropout(0),
                    tf.keras.layers.Dense(9, activation='softmax')
                ])
        if typeOfModel == 'modelv56' or typeOfModel == 'modelv56_AD':
            with tf.device('/GPU:0'):

                model = tf.keras.Sequential()

                # Capa de entrada
                model.add(tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(110, 173, 1)))

                # Capas convolucionales
                model.add(tf.keras.layers.Conv2D(192, 3, activation='relu'))
                model.add(tf.keras.layers.Conv2D(224, 3, activation='relu'))
                model.add(tf.keras.layers.Conv2D(128, 3, activation='relu'))
                model.add(tf.keras.layers.Conv2D(160, 3, activation='relu'))

                # Capas densas
                model.add(tf.keras.layers.Flatten())
                model.add(tf.keras.layers.Dense(128, activation='relu'))
                model.add(tf.keras.layers.Dense(96, activation='relu'))
                model.add(tf.keras.layers.Dense(32, activation='relu'))
                model.add(tf.keras.layers.Dense(192, activation='relu'))

                # Capa de salida
                model.add(tf.keras.layers.Dense(9, activation='softmax'))

        if typeOfModel == 'modelv57' or typeOfModel == 'modelv57_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential()

                # Capa de entrada
                model.add(tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(110, 173, 1)))
                model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

                # Capas convolucionales
                model.add(tf.keras.layers.Conv2D(192, 3, activation='relu'))
                model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
                model.add(tf.keras.layers.Conv2D(224, 3, activation='relu'))
                model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
                model.add(tf.keras.layers.Conv2D(128, 3, activation='relu'))
                model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
                model.add(tf.keras.layers.Conv2D(160, 3, activation='relu'))

                # Capas densas
                model.add(tf.keras.layers.Flatten())
                model.add(tf.keras.layers.Dense(128, activation='relu'))
                model.add(tf.keras.layers.Dense(96, activation='relu'))
                model.add(tf.keras.layers.Dense(32, activation='relu'))
                model.add(tf.keras.layers.Dense(192, activation='relu'))

                # Capa de salida
                model.add(tf.keras.layers.Dense(9, activation='softmax'))

        if typeOfModel == 'modelv58' or typeOfModel == 'modelv58_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential()

                # Capa de entrada
                model.add(tf.keras.layers.Conv2D(128, 5, activation='relu', input_shape=(110, 173, 1)))
                model.add(tf.keras.layers.Dropout(0.0))

                # Capa convolucional 1
                model.add(tf.keras.layers.Conv2D(64, 5, activation='relu'))
                model.add(tf.keras.layers.Dropout(0.0))

                # Capa densa 1
                model.add(tf.keras.layers.Flatten())
                model.add(tf.keras.layers.Dense(200, activation='relu'))
                model.add(tf.keras.layers.Dropout(0.3))

                # Capa densa 2
                model.add(tf.keras.layers.Dense(100, activation='relu'))
                model.add(tf.keras.layers.Dropout(0.3))

                # Capa densa 3
                model.add(tf.keras.layers.Dense(500, activation='relu'))
                model.add(tf.keras.layers.Dropout(0.3))

                # Capa densa 4
                model.add(tf.keras.layers.Dense(250, activation='relu'))
                model.add(tf.keras.layers.Dropout(0.6))

                # Capa convolucional 2
                model.add(tf.keras.layers.Conv2D(128, 5, activation='relu'))
                model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

                # Capa convolucional 3
                model.add(tf.keras.layers.Conv2D(64, 5, activation='relu'))
                model.add(tf.keras.layers.Dropout(0.0))

                # Capa de salida
                model.add(tf.keras.layers.Flatten())
                model.add(tf.keras.layers.Dense(9, activation='softmax'))

                # Compilar el modelo
                optimizer = tf.keras.optimizers.Adam(learning_rate=0.0021263151446712435)
                model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

                return model
        if typeOfModel == 'modelv59' or typeOfModel == 'modelv59_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential()
                model.add(tf.keras.layers.Conv2D(32, 2, activation='relu', input_shape=(110, 173, 1)))
                model.add(tf.keras.layers.MaxPooling2D((2, 2)))
                model.add(tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'))
                model.add(tf.keras.layers.MaxPooling2D((2, 2)))
                model.add(tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same'))
                model.add(tf.keras.layers.MaxPooling2D((2, 2)))

                model.add(tf.keras.layers.Flatten())

                model.add(tf.keras.layers.Dense(200, activation='relu'))
                model.add(tf.keras.layers.Dropout(0.3))
                model.add(tf.keras.layers.Dense(100, activation='relu'))
                model.add(tf.keras.layers.Dropout(0.3))

                model.add(tf.keras.layers.Dense(9, activation='softmax'))

                model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0020477),
                            loss='categorical_crossentropy',
                            metrics=['accuracy'])

                return model

        if typeOfModel == 'modelv60' or typeOfModel == 'modelv60_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential()

                # input_units: 128
                # input_kernel: 2
                model.add(Conv2D(128, 2, activation='relu', input_shape=(110, 173, 1)))
                model.add(MaxPooling2D((2, 2)))
                model.add(Flatten())
                model.add(Dense(250, activation='relu'))
                model.add(Dropout(0.3))
                model.add(Dense(9, activation='softmax'))
                model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                            loss='categorical_crossentropy',
                            metrics=['accuracy'])

                return model
        if typeOfModel == 'modelv61' or typeOfModel == 'modelv61_AD':
            with tf.device('/GPU:0'):
                model = tf.keras.Sequential()

                # input_units: 128
                # input_kernel: 2
                model.add(tf.keras.layers.Conv2D(192, (2, 2), activation='relu', input_shape=(110, 173, 1)))
                model.add(tf.keras.layers.MaxPooling2D((2, 2)))
                model.add(tf.keras.layers.Conv2D(192, (2, 2), activation='relu'))
                model.add(tf.keras.layers.MaxPooling2D((2, 2)))
                model.add(tf.keras.layers.Conv2D(96, (3, 3), activation='relu'))
                model.add(tf.keras.layers.MaxPooling2D((2, 2)))
                model.add(Dropout(0.6))
                model.add(tf.keras.layers.Flatten())
                model.add(Dense(250, activation='relu'))
                model.add(Dense(9, activation='softmax'))
                model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                            loss='categorical_crossentropy',
                            metrics=['accuracy'])

                return model


        model.compile(optimizer='adam',
                      loss='categorical_crossentropy', metrics=['accuracy'])

        print(model.summary())
        return model

    def prepare_logs(self, typeOfModel):
        # definir la ruta de los logs
        log_dir = "logs/fit/" + typeOfModel  # agregar el nombre del modelo
        tensorboard_callback = tf.keras.callbacks.TensorBoard(
            log_dir=log_dir, histogram_freq=1, update_freq='epoch')
        return tensorboard_callback

    def prepare_model_checkpoint(self, typeOfModel, EPOCHS):
        # definir la ruta de guardado del modelo
        # agregar el nombre del modelo
        # checkpoint_filepath = "./models/{}__model-{{epoch:02d}}-{{val_accuracy:.4f}}.h5".format(typeOfModel)
        checkpoint_filepath = "./models/{}__model-{}-{}-epochs.h5".format(
            typeOfModel, typeOfModel, EPOCHS)
        model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_filepath,
            save_weights_only=False,
            monitor='val_accuracy',
            mode='max',
            save_best_only=True)
        return model_checkpoint_callback

    def prepare_early_stopping(self):
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=3, verbose=1, mode='min')
        return early_stopping

    def training(self):
        fileName = "marv1"
        FILE_NAME = fileName + "_clean"
        EPOCHS = 100
        last_epoch = 0
        MODEL_N = 'modelv1'
        MODEL_NAME = FILE_NAME + '-{}-{}-epochs.h5'.format(MODEL_N, EPOCHS)

        self.clean_data(fileName)
        training_data = self.prepare_training_data(FILE_NAME, False)
        # training_data_AD = self.prepare_training_data(FILE_NAME, True)

        # len(x_train):  7338
        # len(y_train):  7338
        # len(x_validate):  816
        # len(y_validate):  816

        # check if GPU is available
        print("Num GPUs Available: ", len(
            tf.config.list_physical_devices('GPU')))

        # print tensorflow version
        print('Tensorflow version: ', tf.__version__)
        # modelv22
        models = [ 'modelv61', 'modelv26', 'modelv49']
        # models = ['modelv49']

        # # get all models names and add suffix _AD and and in array
        # models_AD = []
        # for modelName in models:
        #     models_AD.append(modelName + '_AD')

        # # add models_AD to models
        # models = models + models_AD
        if 1 == 1:
            for modelName in models:
                model = self.prepare_model(modelName)
                tensorboard_callback = self.prepare_logs(modelName)
                model_checkpoint_callback = self.prepare_model_checkpoint(
                    modelName, EPOCHS)
                early_stopping = self.prepare_early_stopping()

            # separar los datos de entrenamiento y validación
                if modelName.endswith('_AD'):
                    (x_train, y_train), (x_validate,
                                        y_validate)= training_data_AD
                else:
                    (x_train, y_train), (x_validate,
                                    y_validate) = training_data

            #     # entrenar el modelo
                model.fit(x_train, y_train, epochs=EPOCHS, batch_size=32, validation_data=(x_validate, y_validate), callbacks=[
                        tensorboard_callback, model_checkpoint_callback, early_stopping], initial_epoch=last_epoch)

        # evaluar el modelo
        (x_train, y_train), (x_validate,
                                    y_validate) = training_data
        for modelName in models:
            model = keras.models.load_model(
                './models/{}__model-{}-{}-epochs.h5'.format(modelName, modelName, EPOCHS), compile=False)
            # compile model
            model.compile(optimizer='adam',
                            loss='categorical_crossentropy', metrics=['accuracy'])
            print('Evaluating model: ', modelName)
            evaluation = model.evaluate(x_validate, y_validate, verbose=2)
            print('Test loss:', evaluation[0])
            print('Test accuracy:', evaluation[1])
            print('----------------------------------')


training = TrainingModel()
training.training()


# C:\Users\Alex\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\tensorboard.exe --host 0.0.0.0 --logdir path\to\immortal_xinofarmer\inc\scripts\MAIN\logs
