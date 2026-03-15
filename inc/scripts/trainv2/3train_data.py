import numpy as np
import os
from models import otherception3 as googlenet
from random import shuffle
from pathlib import Path
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import cv2


WIDTH = 173
HEIGHT = 110
LR = 1e-3
EPOCHS = 30
FILE_NAME = "zavainGPU"
BEST_VAL_ACC = -1
MODEL_N = 'otherception3v3'


MODEL_NAME = FILE_NAME + \
    '-{}-{}-{}-epochs.model'.format(LR, MODEL_N, EPOCHS)

data_dir = Path('./data') / FILE_NAME
model_dir = Path('./models')
model_file = model_dir / MODEL_NAME

# model = googlenet(WIDTH, HEIGHT, LR, 9)
model = googlenet(WIDTH, HEIGHT, 3, LR, output=9, model_name=MODEL_NAME)

# check if ./models/ folder exists
if not model_dir.exists():
    model_dir.mkdir()

# check if model exists
if os.path.isfile('./models/' + MODEL_NAME + '.meta'):
    print('Model exists, loading previous model {}'.format(MODEL_NAME))
    model.load(model_file)
    print('Model loaded!')


for i in range(EPOCHS):
	# get all files from data_dir
	files = [str(f) for f in data_dir.glob('*.npy')]

	number_of_files = len(files)
        
	# load 100 files at a time
	for i in range(0, number_of_files, 100):
             
		# get 100 files
		batch_files = files[i:i+100]
		train_data = None
                
		# load all files into memory
		for f in batch_files:
			print('Loading file {}'.format(f))
			data = np.load(f, allow_pickle=True)
			if train_data is None:
				train_data = data
			else:
				train_data = np.concatenate((train_data, data))
		
		shuffle(train_data)
                                
		print('Loaded {} training data'.format(len(train_data)))
            
		train = train_data[:-1000]
		test = train_data[-1000:]

		X = np.array([i[0] for i in train]).reshape(-1, HEIGHT, WIDTH, 1)
		Y = [i[1] for i in train]

		test_x = np.array([i[0] for i in test]).reshape(-1, HEIGHT, WIDTH, 1)
		test_y = [i[1] for i in test]

		# Entrena el modelo
		model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),
				snapshot_step=500, show_metric=True, run_id=MODEL_NAME, batch_size=100, shuffle=True)

		# Guarda el modelo
		model.save(model_file)

		# Calcula la precisión del modelo
		val_acc = model.predict(test_x)
		val_acc = np.mean(np.argmax(val_acc, 1) == np.argmax(test_y, 1))
		print('Validation accuracy: {}'.format(val_acc))

		# Si la precisión es mejor que la anterior, guarda el modelo
		if val_acc > BEST_VAL_ACC:
			print('New best validation accuracy! Saving model...')
			BEST_VAL_ACC = val_acc
			model.save(model_dir / f'best_{MODEL_NAME}')


# C:\Users\Alex\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\tensorboard.exe --logdir path\to\immortal_xinofarmer\inc\scripts\trainv2\log
