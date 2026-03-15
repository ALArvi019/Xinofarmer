from windowcapture import WindowCapture
from preprocess import PreProcessImage
import cv2 as cv
from time import time
from time import sleep
import os

WINDOW_NAME = 'Toxic Lurker - NPC - Diablo Immortal - Google Chrome'

# BEAST_NAME = 'Toxic Lurker' (split WINDOW_NAME to get this)

BEAST_NAME = 'Toxic_Lurker'

LastFileNumber = 0

wincap = WindowCapture('Toxic Lurker - NPC - Diablo Immortal - Google Chrome')
preprocess = PreProcessImage()

# check if ./data directory exists
if not os.path.exists('./data'):
	os.makedirs('./data')

# check if ./data/BEAST_NAME directory exists
if not os.path.exists('./data/{}'.format(BEAST_NAME)):
	os.makedirs('./data/{}'.format(BEAST_NAME))
else:
	# find the last file number
	LastFileNumber = len(os.listdir('./data/{}'.format(BEAST_NAME)))

for i in list(range(4))[::-1]:
        print(i+1)
        sleep(1)
	
captured_images = []

while True:
	screenshot = wincap.get_screenshotBrowser()

	screenshot = preprocess.crop(screenshot, 500, 200, 1000, 700)

	# display the processed image
	cv.imshow('Computer Vision', screenshot)

	# save image to ./data/BEAST_NAME
	cv.imwrite('./data/{}/{}_{}.png'.format(BEAST_NAME, BEAST_NAME, LastFileNumber), screenshot)

	LastFileNumber += 1

	# debug the loop rate
	# print('FPS {}'.format(1 / (time.time() - last_time)))
	# last_time = time.time()

	# press 'q' with the output window focused to exit.
	# waits 1 ms every loop to process key presses
	if cv.waitKey(1) == ord('q'):
		cv.destroyAllWindows()
		break