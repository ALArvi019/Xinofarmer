import numpy as np
import os
import cv2 as cv



fileName = "tundra"
starting_value = 1

while True:
	file_name = './data/' + fileName + '/' + \
                            fileName + '-{}.npy'.format(starting_value)

	if os.path.isfile(file_name):
		print('File exists {} , loading previous data!'.format(file_name))
		training_data = np.load(file_name, allow_pickle=True)

		# show all images in training_data
		for data in training_data:
			img = data[0]
			choice = data[1]
			cv.imshow('test', img)
			print(choice)
			if cv.waitKey(25) & 0xFF == ord('q'):
				cv.destroyAllWindows()
				break


		starting_value += 1
	else:
		print('File does not exist, Finishing!')
		
		break