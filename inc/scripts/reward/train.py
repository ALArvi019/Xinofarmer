import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.optimizers import Adam
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

class TrainModel:
	def __init__(self, model_name):
		self.model_name = model_name

		# load the model or create a new one
		try:
			self.model = keras.models.load_model(self.model_name)
		except OSError:
			print('No model found, creating a new one')
			# Modelo secuencial
			self.model = Sequential()

			# Capa de Convolución
			self.model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(80, 80, 1)))

			# Capa de aplanamiento
			self.model.add(Flatten())

			# Capa totalmente conectada
			self.model.add(Dense(128, activation='relu'))

			# Capa de salida
			self.model.add(Dense(8, activation='softmax'))

			# Compilar el modelo
			self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

	def predict(self, image, epsilon, random):
		# image = np.squeeze(image, axis=0)
		# plt.figure()
		# plt.imshow(image)
		# plt.colorbar()
		# plt.grid(False)
		# plt.show()
		if np.random.rand() <= epsilon and random == True:
			# generate random prediction [[0. 0. 0. 0. 0. 0. 0. 0.]]
			return np.random.rand(1, 8)
		else:
			# toma la acción con mayor probabilidad según el modelo
			return self.model.predict(image, verbose=0)
		

	def action(self, prediction):
		# example of prediction: [[0.0000000e+00 1.1824496e-28 1.2519549e-27 4.2893185e-36 1.0000000e+00 8.7315163e-37 3.7914796e-37 8.4954241e-20]]
		# the action with the highest probability is chosen
		return np.argmax(prediction)

	def action_random(self):
		# choose a random action
		return np.random.randint(0, 8)

	def save(self, model_name, screen, target):
		history = self.model.fit(screen, target, epochs=10)
		self.model.save(model_name)

		# Guardar la información de la historia de entrenamiento
		loss = history.history['loss']
		acc = history.history['accuracy']

		# print('loss: ', loss)
		# print('acc: ', acc)

		# # Graficar la pérdida de entrenamiento
		# plt.plot(loss)
		# plt.title('Pérdida por época')
		# plt.ylabel('Pérdida')
		# plt.xlabel('Época')
		# plt.show()

		# # Graficar la precisión de entrenamiento
		# plt.plot(acc)
		# plt.title('Precisión por época')
		# plt.ylabel('Precisión')
		# plt.xlabel('Época')
		# plt.show()


	def get_reward(self, last_frames, gray, lines, player_x, player_y, player_size):
		reward = 0

		if len(last_frames) > 2:
			# remove the first frame from the list
			last_frames.pop(0)

			# calculate the mean squared error between all the frames
			mean_squared_error = np.mean([np.sum((gray - frame) ** 2) for frame in last_frames])

			# set a threshold for the mean squared error
			threshold = 10 ** 6

			if mean_squared_error < threshold:
				# the frames are too similar, do something (e.g. break the loop)
				reward += -10
			else:
				reward += +10


		# if the last 5 frames in last_frames are equal images then the reward is -100
		# if last_frames is not None and len(last_frames) >= 5:
		# 	if np.array_equal(last_frames[0], last_frames[1]) and np.array_equal(last_frames[1], last_frames[2]) and np.array_equal(last_frames[2], last_frames[3]) and np.array_equal(last_frames[3], last_frames[4]):
		# 		reward += -30
		# 	else:
		# 		reward += +100
		# 	last_frames.pop(0)

		# check if player collisisons with lines
		if lines is not None:
			for line in lines:
				x1, y1, x2, y2 = line[0]
				if (x1 - player_x)**2 + (y1 - player_y)**2 <= player_size**2:
					reward += -5
				if (x2 - player_x)**2 + (y2 - player_y)**2 <= player_size**2:
					reward += -5

		return reward



