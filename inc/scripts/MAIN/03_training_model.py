import os
import numpy as np
import shutil
import tensorflow as tf
import tkinter as tk
import sys
from tkinter import simpledialog
from tensorflow.keras import layers, models
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard, EarlyStopping

# Define your labels as lists
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

class TrainingModel:

    def __init__(self):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        base_path_tmp = base_path
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(base_path, 'config.txt')
        self.icon_path = os.path.join(base_path_tmp, 'xf.ico')
        self.old_model = 'cement'
        self.mapname = self.ask_for_mapname()
        self.new_training = True
        

    def ask_for_mapname(self):
        default_window_name, default_file_name_prefix = self.load_config()
        root = tk.Tk()
        if os.path.exists(self.icon_path):
            root.iconbitmap(default=self.icon_path)
        else:
            print("Icon file not found at the specified path.")
        root.withdraw()  # Hide the main tkinter window
        mapname = simpledialog.askstring("Input", "Enter the file name (without extension):", initialvalue=default_file_name_prefix)
        root.destroy()  # Destruye la ventana después de obtener el nombre del mapa
        return mapname
    
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                lines = f.read().splitlines()
                if len(lines) >= 2:
                    return lines[0], lines[1]
                elif len(lines) == 1:
                    return lines[0], ""
        return "", ""

    def clean_data(self, fileName, merge=False):
        print("CLEAN DATA")
        starting_value = 1
        training_data = []
        while True:
            file_name = f'./data/{self.mapname}/{fileName}-{starting_value}.xin'

            if os.path.isfile(file_name):
                training_data_tmp = np.load(file_name, allow_pickle=True)
                print('training_data_tmp: ', len(training_data_tmp))
                training_data.extend(training_data_tmp)
                print('training_data: ', len(training_data))
                starting_value += 1
            else:
                break

        print('training_data before: ', len(training_data))
        before = len(training_data)

        if not merge:
            unique_data = {}
            for data in training_data:
                img, choice = data
                hash_value = hash(str(img.tolist()) + str(choice))

                if hash_value in unique_data:
                    if any(np.array_equal(img, d[0]) and np.array_equal(choice, d[1]) for d in unique_data[hash_value]):
                        continue
                    unique_data[hash_value].append(data)
                else:
                    unique_data[hash_value] = [data]

            training_data = [(d[0], d[1]) for data_list in unique_data.values() for d in data_list]
            print('training_data after: ', len(training_data))

        training_data = np.array(training_data, dtype=object)

        if not os.path.exists(f'./data/{fileName}_clean'):
            os.makedirs(f'./data/{fileName}_clean')
        np.save(f'./data/{fileName}_clean/{fileName}_clean-1', training_data)
        print("CLEAN DATA DONE")

    def prepare_training_data(self, FILE_NAME):
        data = np.load(f'./data/{FILE_NAME}_clean/{FILE_NAME}_clean-1.xin', allow_pickle=True)
        data_eval = np.load(f'./data/{FILE_NAME}_clean/{FILE_NAME}_eval-1.xin', allow_pickle=True)

        # Separar las imágenes y etiquetas
        x = data[:, 0]
        y = data[:, 1]

        # get shape of image for reshape
        print('image_shape:', x[0].shape)

        # Convertir las imágenes a un array numpy
        x_train = np.array([i for i in x]).reshape(-1, 110, 173, 1)

        # convertir las etiquetas a un array numpy dtype=uint8
        y_train = np.array([i for i in y])

        print(x_train.shape)

        # Separar las imágenes y etiquetas
        x_eval = data_eval[:, 0]
        y_eval = data_eval[:, 1]

        # Convertir las imágenes a un array numpy
        x_eval = np.array([i for i in x_eval]).reshape(-1, 110, 173, 1)

        # convertir las etiquetas a un array numpy dtype=uint8
        y_eval = np.array([i for i in y_eval])

        print(x_eval.shape)

        x_train = x_train / 255.0
        x_eval = x_eval / 255.0

        # mezclar los datos
        indices = np.arange(len(x_train))
        np.random.shuffle(indices)
        x_train = x_train[indices]
        y_train = y_train[indices]

        print('len(x_train): ', len(x_train))
        print('len(y_train): ', len(y_train))
        print('len(x_eval): ', len(x_eval))
        print('len(y_eval): ', len(y_eval))

        return (x_train, y_train), (x_eval, y_eval)
            


    def prepare_model(self, typeOfModel):
        if self.new_training:
            if typeOfModel == 'modelv61':
                model = models.Sequential([
                    Conv2D(192, (2, 2), activation='relu', input_shape=(110, 173, 1)),
                    MaxPooling2D((2, 2)),
                    Conv2D(192, (2, 2), activation='relu'),
                    MaxPooling2D((2, 2)),
                    Conv2D(96, (3, 3), activation='relu'),
                    MaxPooling2D((2, 2)),
                    Dropout(0.6),
                    Flatten(),
                    Dense(250, activation='relu'),
                    Dense(9, activation='softmax')
                ])
                model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                              loss='categorical_crossentropy',
                              metrics=['accuracy'])
                return model
        else:
            model = tf.keras.models.load_model(f'./data/{self.old_model}.h5', compile=False)
            model.compile(optimizer='adam',
                          loss='categorical_crossentropy', metrics=['accuracy'])
            print('Model loaded!')
            return model

    def prepare_logs(self, typeOfModel):
        log_dir = f"logs/fit/{typeOfModel}"
        tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1, update_freq='epoch')
        return tensorboard_callback

    def prepare_model_checkpoint(self, typeOfModel, EPOCHS):
        checkpoint_filepath = f"./data/{typeOfModel}__model-{typeOfModel}-{EPOCHS}-epochs_{self.mapname}.h5"
        model_checkpoint_callback = ModelCheckpoint(
            filepath=checkpoint_filepath,
            save_weights_only=False,
            monitor='val_accuracy',
            mode='max',
            save_best_only=True)
        return model_checkpoint_callback

    def prepare_early_stopping(self):
        early_stopping = EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='min')
        return early_stopping

    def training(self):
        fileName = self.mapname
        FILE_NAME = fileName
        EPOCHS = 100
        last_epoch = 0
        models_to_train = ['modelv61']

        self.clean_data(fileName, True)
        training_data = self.prepare_training_data(FILE_NAME)

        print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
        print('Tensorflow version: ', tf.__version__)

        for modelName in models_to_train:
            model = self.prepare_model(modelName)
            tensorboard_callback = self.prepare_logs(modelName)
            model_checkpoint_callback = self.prepare_model_checkpoint(modelName, EPOCHS)
            early_stopping = self.prepare_early_stopping()

            (x_train, y_train), (x_validate, y_validate) = training_data

            model.fit(x_train, y_train, epochs=EPOCHS, batch_size=6, validation_data=(x_validate, y_validate),
                      callbacks=[tensorboard_callback, model_checkpoint_callback, early_stopping], initial_epoch=last_epoch)

        data_test = np.load(f'./data/{FILE_NAME}_clean/{FILE_NAME}_test-1.xin', allow_pickle=True)
        x_test = np.array([i[0] for i in data_test]).reshape(-1, 110, 173, 1)
        y_test = np.array([i[1] for i in data_test])

        x_test = x_test / 255.0

        for modelName in models_to_train:
            model = tf.keras.models.load_model(
                f'./data/{modelName}__model-{modelName}-{EPOCHS}-epochs_{self.mapname}.h5', compile=False)
            model.compile(optimizer='adam',
                          loss='categorical_crossentropy', metrics=['accuracy'])
            print('Evaluating model: ', modelName)
            evaluation = model.evaluate(x_test, y_test, verbose=2)
            print('Test loss:', evaluation[0])
            print('Test accuracy:', evaluation[1])
            print('----------------------------------')
            shutil.move(f'./data/{modelName}__model-{modelName}-{EPOCHS}-epochs_{self.mapname}.h5',
                        f'./data/model_{self.mapname}.dat')
            # print your model has been trained and tested successfully
            # press any jey to exit
            input("Press Enter to continue...")
            break

if __name__ == "__main__":
    training = TrainingModel()
    training.training()
