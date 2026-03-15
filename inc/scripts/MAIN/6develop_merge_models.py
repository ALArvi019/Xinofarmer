!nvidia-smi
!pip install keras-tuner --upgrade
from google.colab import drive
drive.mount('/content/drive')
!ls /content/drive/
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
        self.old_model = 'ancients'
        self.mapname = "common_models"
        self.new_training=False


    def clean_data(self, fileName, merge=False):
        # CLEAN DATA
        print("CLEAN DATA")
        starting_value = 1
        training_data = []
        while True:
            file_name = '/content/drive/MyDrive/COLAB/TRAIN/'+self.mapname+'/' + fileName + '-{}.npy'.format(starting_value)

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
        before = len(training_data)

        if merge is False:

            unique_data = {}

            for data in training_data:
                img = data[0]
                choice = data[1]

                # calculate unique hash for img + choice
                hash_value = hash(str(img.tolist()) + str(choice))

                # print unique_data len / training_data len
                print(len(unique_data), '/', len(training_data))

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

            print('training_data before: ', before)
            print('training_data after: ', len(training_data))

        training_data = np.array(training_data, dtype=object)

        # create folder if not exists
        if not os.path.exists('/content/drive/MyDrive/COLAB/TRAIN/' + fileName + '_clean'):
            os.makedirs('/content/drive/MyDrive/COLAB/TRAIN/' + fileName + '_clean')
        np.save('/content/drive/MyDrive/COLAB/TRAIN/' + fileName + '_clean' + '/' +
                fileName + '_clean-1', training_data)
        training_data = []
        # CLEAN DATA
        print("CLEAN DATA DONE")

    def prepare_training_data(self, FILE_NAME, imageGen=False):

        # carga los datos
        data = np.load('/content/drive/MyDrive/COLAB/TRAIN/{}/{}-1.npy'.format(FILE_NAME,
                       FILE_NAME), allow_pickle=True)

        # Separar las imágenes y etiquetas
        x = data[:, 0]
        y = data[:, 1]

        # get shape of image for reshape
        print('image_shape:', x[0].shape)

        # Convertir las imágenes a un array numpy
        x = np.array([i for i in x]).reshape(-1, 110, 173, 1)

        # convertir las etiquetas a un array numpy dtype=uint8
        y = np.array([i for i in y])

        print(x.shape)

        # Separar los datos en un conjunto de entrenamiento y validación
        x_train, y_train = x, y
        #x_train, x_validate, y_train, y_validate = train_test_split(
        #    x_train_val, y_train_val, test_size=0.05, random_state=42)

        # carga los datos
        data = np.load('/content/drive/MyDrive/COLAB/TRAIN/{}_eval/{}_eval-1.npy'.format(FILE_NAME, FILE_NAME), allow_pickle=True)

         # Separar las imágenes y etiquetas
        x = data[:, 0]
        y = data[:, 1]

        # Convertir las imágenes a un array numpy
        x = np.array([i for i in x]).reshape(-1, 110, 173, 1)

        # convertir las etiquetas a un array numpy dtype=uint8
        y = np.array([i for i in y])

        print(x.shape)

        # Separar los datos en un conjunto de entrenamiento y validación
        x_validate, y_validate = x, y

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

        if self.new_training is True:

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
        else:
            model = keras.models.load_model(
                '/content/drive/MyDrive/COLAB/TRAIN/OLD/{}.dat'.format(self.old_model), compile=False)
            # compile model
            model.compile(optimizer='adam',
                            loss='categorical_crossentropy', metrics=['accuracy'])
            print('Model loaded!')
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
        checkpoint_filepath = "/content/drive/MyDrive/COLAB/TRAIN/{}__model-{}-{}-epochs_{}.h5".format(
            typeOfModel, typeOfModel, EPOCHS, self.mapname)
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
        fileName = self.mapname
        FILE_NAME = fileName + "_clean"
        EPOCHS = 100
        last_epoch = 0
        MODEL_N = 'modelv1'
        MODEL_NAME = FILE_NAME + '-{}-{}-epochs.h5'.format(MODEL_N, EPOCHS)

        self.clean_data(fileName, True)
        training_data = self.prepare_training_data(FILE_NAME, False)

        print("Num GPUs Available: ", len(
            tf.config.list_physical_devices('GPU')))

        print('Tensorflow version: ', tf.__version__)
        models = [ 'modelv61']


        if 1 == 1:
            for modelName in models:
                model = self.prepare_model(modelName)
                tensorboard_callback = self.prepare_logs(modelName)
                model_checkpoint_callback = self.prepare_model_checkpoint(
                    modelName, EPOCHS)
                early_stopping = self.prepare_early_stopping()


                (x_train, y_train), (x_validate,
                                    y_validate) = training_data

            #     # entrenar el modelo
                model.fit(x_train, y_train, epochs=EPOCHS, batch_size=6, validation_data=(x_validate, y_validate), callbacks=[
                        tensorboard_callback, model_checkpoint_callback, early_stopping], initial_epoch=last_epoch)

        # evaluar el modelo
        data = np.load('/content/drive/MyDrive/COLAB/TRAIN/{}_test/{}_test-1.npy'.format(FILE_NAME,
                       FILE_NAME), allow_pickle=True)

         # Separar las imágenes y etiquetas
        x = data[:, 0]
        y = data[:, 1]

        # Convertir las imágenes a un array numpy
        x = np.array([i for i in x]).reshape(-1, 110, 173, 1)

        # convertir las etiquetas a un array numpy dtype=uint8
        y = np.array([i for i in y])

        print(x.shape)

        # Separar los datos en un conjunto de entrenamiento y validación
        x_test, y_test = x, y

        x_test = x_test / 255.0

        for modelName in models:
            model = keras.models.load_model(
                '/content/drive/MyDrive/COLAB/TRAIN/{}__model-{}-{}-epochs_{}.h5'.format(modelName, modelName, EPOCHS, self.mapname), compile=False)
            # compile model
            model.compile(optimizer='adam',
                            loss='categorical_crossentropy', metrics=['accuracy'])
            print('Evaluating model: ', modelName)
            evaluation = model.evaluate(x_test, y_test, verbose=2)
            print('Test loss:', evaluation[0])
            print('Test accuracy:', evaluation[1])
            print('----------------------------------')


training = TrainingModel()
training.training()


# C:\Users\Alex\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\tensorboard.exe --host 0.0.0.0 --logdir path\to\immortal_xinofarmer\inc\scripts\MAIN\logs
