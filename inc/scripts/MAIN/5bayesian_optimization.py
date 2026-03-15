!nvidia-smi
!pip install keras-tuner --upgrade
from google.colab import drive
drive.mount('/content/drive')
!ls /content/drive/
import tensorflow as tf
from tensorflow import keras
import kerastuner as kt
from kerastuner import RandomSearch
from kerastuner.engine.hyperparameters import HyperParameters
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF


# make keras-tunner work

# Path: inc\scripts\MAIN\5bayesian_optimization.py

class BayesianTuner(kt.BayesianOptimization):
    def __init__(self, hypermodel, **kwargs):
        super().__init__(hypermodel, **kwargs)

    def run_trial(self, trial, *args, **kwargs):
        hp = trial.hyperparameters
        model = self.hypermodel.build(hp)
        return self.hypermodel.fit(hp, model, *args, **kwargs)

def prepare_training_data(FILE_NAME, imageGen=False):

        # carga los datos
        # data = np.load('./data/{}/{}-1.npy'.format(FILE_NAME,
        #                FILE_NAME), allow_pickle=True)
        data = np.load('/content/drive/MyDrive/COLAB/marv1_clean-1.npy', allow_pickle=True)

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

        # Separar los datos en un conjunto de entrenamiento, validación y prueba
        x_train_val, x_test, y_train_val, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42)
        x_train, x_validate, y_train, y_validate = train_test_split(
            x_train_val, y_train_val, test_size=0.25, random_state=42)  # test_size=0.25 porque 0.2 * 0.8 = 0.16

        x_train = x_train / 255.0
        x_validate = x_validate / 255.0
        x_test = x_test / 255.0

        # mezclar los datos
        indices = np.arange(len(x_train))
        np.random.shuffle(indices)
        x_train = x_train[indices]
        y_train = y_train[indices]

        print('len(x_train): ', len(x_train))
        print('len(y_train): ', len(y_train))
        print('len(x_validate): ', len(x_validate))
        print('len(y_validate): ', len(y_validate))
        print('len(x_test): ', len(x_test))
        print('len(y_test): ', len(y_test))

        return (x_train, y_train), (x_validate, y_validate), (x_test, y_test)


def build_model(hp):
    model = tf.keras.Sequential()

    # model.add(tf.keras.layers.Conv2D(
    #     hp.Int('input_units', min_value=32, max_value=256, step=32),
    #     hp.Choice('input_kernel', values=[2, 3]),
    #     activation='relu',
    #     input_shape=(110, 173, 1)
    # ))

    # model.add(tf.keras.layers.MaxPooling2D((2, 2)))

    # num_conv_layers = hp.Int('num_conv_layers', min_value=0, max_value=3, default=2)
    # num_dense_layers = hp.Int('num_dense_layers', min_value=0, max_value=2, default=1)

    # for i in range(num_conv_layers):
    #     filters = hp.Choice(f'conv_{i+1}_filters', values=[32, 64, 128])
    #     kernel_size = hp.Choice(f'conv_{i+1}_kernel_size', values=[2, 3])
    #     activation = hp.Choice(f'conv_{i+1}_activation', values=['relu'])
    #     model.add(tf.keras.layers.Conv2D(filters, kernel_size, activation=activation, padding='same'))
    #     model.add(tf.keras.layers.MaxPooling2D((2, 2)))

    # model.add(tf.keras.layers.Flatten())

    # for i in range(num_dense_layers):
    #     units = hp.Int(f'dense_{i+1}_units', min_value=50, max_value=300, step=50)
    #     activation = hp.Choice(f'dense_{i+1}_activation', values=['relu'])
    #     dropout_rate = hp.Float(f'dropout_{i+1}', min_value=0.0, max_value=0.8, step=0.3)
    #     model.add(tf.keras.layers.Dense(units, activation=activation))
    #     model.add(tf.keras.layers.Dropout(dropout_rate))

    # model.add(tf.keras.layers.Dense(9, activation='softmax'))

    # model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    #               loss='categorical_crossentropy',
    #               metrics=['accuracy'])


    # ------------------------------
    
    model.add(tf.keras.layers.Conv2D(192, (2, 2), activation='relu', input_shape=(110, 173, 1)))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    model.add(tf.keras.layers.Conv2D(192, (2, 2), activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    model.add(tf.keras.layers.Conv2D(96, (3, 3), activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    # model.add(tf.keras.layers.Dropout(hp.Float('dropout_1', min_value=0.0, max_value=0.8, step=0.2)))
    model.add(tf.keras.layers.Dropout(hp.Choice('dropout_1', values=[0.0, 0.2, 0.4, 0.6, 0.8])))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(hp.Float('dense_1', min_value=0, max_value=300, step=25), activation='relu'))
    model.add(tf.keras.layers.Dense(9, activation='softmax'))
         
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])
    return model


# Path: inc\scripts\MAIN\5bayesian_optimization.py




# define the search space
tuner_search = BayesianTuner(
    build_model,
    objective='val_accuracy',
    max_trials=6000,
    directory='/content/drive/MyDrive/COLAB',
    project_name='marv1_clean_0_4'
)


# print the search space summary
tuner_search.search_space_summary()

# print best hyperparameters
tuner_search.results_summary()

# get the training, validation and test data
(x_train, y_train), (x_validate, y_validate), (X_test, y_test) = prepare_training_data('marv1_clean', False)

stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='min')

# perform the hypertuning
tuner_search.search(x=x_train,
                    y=y_train,
                    epochs=100,
                    batch_size=10,
                    validation_data=(x_validate, y_validate),
                    callbacks=[stop_early])



best_trial = tuner_search.oracle.get_best_trials(num_trials=1)[0]

# Obtener el resumen del mejor trial
summary = best_trial.summary()

print(summary)

# Obtener los hiperparámetros completos del mejor trial
hyperparameters = best_trial.hyperparameters.get_config()

# Obtener el orden de las capas
values = best_trial.hyperparameters.values

# # imprimir el orden de las capas
print(values)

# Trial 0005 summary
# Hyperparameters:
# input_units: 192
# input_kernel: 2
# Score: 0.8423615097999573

# Trial 0019 summary
# Hyperparameters:
# input_units: 160
# input_kernel: 2
# Score: 0.8399269580841064

# Trial 0066 summary
# Hyperparameters:
# input_units: 96
# input_kernel: 2
# Score: 0.8368837237358093

# Trial 0023 summary
# Hyperparameters:
# input_units: 160
# input_kernel: 2
# Score: 0.833840548992157

# Trial 0010 summary
# Hyperparameters:
# input_units: 96
# input_kernel: 2
# Score: 0.8326232433319092
# ----------------------------------------------

# Trial 0000 summary
# Hyperparameters:
# input_units_0: 192
# input_units_1: 160
# input_kernel: 2
# Score: 0.8466220498085022

# Trial 0018 summary
# Hyperparameters:
# input_units_0: 160
# input_units_1: 160
# input_kernel: 2
# Score: 0.8454047441482544

# Trial 0011 summary
# Hyperparameters:
# input_units_0: 160
# input_units_1: 192
# input_kernel: 2
# Score: 0.8447961211204529


# ---------------

# Trial 0039 summary
# Hyperparameters:
# input_units_0: 192
# input_units_1: 192
# dropout_1: 0.0
# input_units_2: 96
# input_kernel: 3
# Score: 0.8460133671760559

# Trial 0007 summary
# Hyperparameters:
# input_units_0: 192
# input_units_1: 192
# dropout_1: 0.0
# input_units_2: 128
# input_kernel: 3
# Score: 0.8441874384880066

# Trial 0067 summary
# Hyperparameters:
# input_units_0: 192
# input_units_1: 192
# dropout_1: 0.0
# input_units_2: 128
# input_kernel: 2
# Score: 0.8435788154602051


# -------------------
# Trial 0018 summary
# Hyperparameters:
# dropout_1: 0.6000000000000001
# Score: 0.8387096524238586

# Trial 0010 summary
# Hyperparameters:
# dropout_1: 0.2
# Score: 0.8356664776802063

# Trial 0022 summary
# Hyperparameters:
# dropout_1: 0.8
# Score: 0.8344491720199585

# Trial 0004 summary
# Hyperparameters:
# dropout_1: 0.4
# Score: 0.8314059376716614

# Trial 0012 summary
# Hyperparameters:
# dropout_1: 0.0
# Score: 0.8307973146438599