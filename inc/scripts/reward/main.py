import cv2 as cv
import os
from time import time
from time import strftime
from time import gmtime
import datetime
from windowcapture import WindowCapture
from preprocess import PreProcessImage
from train import TrainModel
from control import Control

loop_time = time()
iterations = 0

resize_multiplier = 6

canny_low_threshold = 0
canny_high_threshold = 30
canny_kernel_dimension = 3

hough_thtreshold = 57
hough_minLineLength = 70
hough_maxLineGap = 20

player_x = 520
player_y = 340
player_size = 25

last_frames = []
total_reward = 0

modelName = 'namari.h5'
random = False

epsilon = 1.0 # probabilidad inicial de exploración
epsilon_min = 0.01 # probabilidad mínima de exploración
decay_rate = 0.995 # tasa de disminución de epsilon

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


wincap = WindowCapture('LDPlayer')
preprocess = PreProcessImage()
train = TrainModel(modelName)
control = Control()



while(True):
	# Resize the screenshot and convert it to grayscale
	screenshot = wincap.get_screenshot()
	screenshot = preprocess.resize(screenshot, screenshot.shape[1]*resize_multiplier, screenshot.shape[0]*resize_multiplier)
	gray = preprocess.to_grayscale(screenshot)

	# Preprocess the image
	edges = preprocess.to_canny(gray, canny_low_threshold, canny_high_threshold, canny_kernel_dimension)
	lines = preprocess.get_lines(edges, hough_thtreshold, hough_minLineLength, hough_maxLineGap)

	# Add the preprocessed image to the list of last frames
	last_frames.append(gray)

	# Get the image ready for training
	train_screenshot = preprocess.image_for_training(screenshot)

	# Use the model to predict the next action
	prediction = train.predict(train_screenshot,epsilon, random)
	action = train.action(prediction)

	# Use the predicted action to control the character
	control.move_character(action)

	# Get the reward for the performed action
	reward = train.get_reward(last_frames, gray, lines, player_x, player_y, player_size)
	total_reward += reward

	# Update the target for the model
	target = prediction
	target[0][action] = reward

	# Save the model with the updated target
	train.save(modelName, train_screenshot, target)

	# every 2 frames show the loop_time in hh:ii:ss and the total reward
	if len(last_frames) % 1 == 0:
		print('Time: {} Total reward: {}'.format(strftime("%H:%M:%S", gmtime(time() - loop_time)), total_reward))
		print('prediction: {}'.format(prediction))
		
	# after 30 iterations show the prediction, action and reward
	if iterations % 30 == 0:
		print('prediction: {}'.format(prediction))
		print('action: {}'.format(action))
		print('reward: {}'.format(reward))


	# disminuye gradualmente epsilon
	epsilon = max(epsilon * decay_rate, epsilon_min)
	iterations += 1

	# ************** /train **************

	preprocess.draw_lines(screenshot, lines, (0, 255, 0), 2)
	preprocess.print_player_position(screenshot, player_x, player_y, player_size, (255, 0, 255), 2)
	preprocess.draw_coliision_between_player_and_lines(screenshot, lines, player_x, player_y, player_size, (0, 0, 255), 2)
	

	preprocess.image_show('screenshot', screenshot)
	preprocess.image_show('edges', edges)
	preprocess.image_show('gray', gray)

	

	# print('FPS {}'.format(1 / (time() - loop_time)))
	# loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
	if cv.waitKey(1) == ord('q'):
		cv.destroyAllWindows()
		break

print('Done.')