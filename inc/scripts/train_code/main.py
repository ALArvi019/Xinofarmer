import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from process import ProcessImage
from path import Path

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
wincap = WindowCapture('LDPlayer')
process = ProcessImage()
path = Path()

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    # screenshot = process.delete_colors(screenshot)
    # screenshot1 = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
    # screenshot1 = process.delete_image_content(screenshot1, 72, 40, 100, 70)
    # screenshot1 = process.delete_image_content(screenshot, 72, 40, 100, 70)
    screenshot = process.toBynary(screenshot)
    collision_matrix = process.get_collision_matrix(screenshot)
    screenshot_collision_matrix_holes = process.draw_collision_matrix(collision_matrix)
    # collision_matrix = process.fill_holes(collision_matrix, screenshot)
    # screenshot_collision_matrix_no_holes = process.draw_collision_matrix(collision_matrix)

	# create start array in 83,57
	# create end array in 1,1
    start = [87, 45]
    end = [1, 1]

	

    path1, dist = path.astar(start, end, collision_matrix.tolist())
    print("Coordenadas que deben ser seguidas:", path1)

    # distance = path.a_star(collision_matrix, start[0], start[1], end[0])
    # path = path.get_path(distance, start[0], start[1], end[0], end[1])

	# draw red point in start
    cv.circle(screenshot_collision_matrix_holes, (start[0], start[1]), 1, (0, 0, 255), 2)

	# draw blue square in 80,50 - 90,60
    cv.rectangle(screenshot_collision_matrix_holes, (72, 40), (100, 70), (255, 0, 0), 2)

    cv.imshow('Result0', screenshot)
    # cv.imshow('Result1', screenshot1)
    cv.imshow('Result2', screenshot_collision_matrix_holes)
    # cv.imshow('Result3', screenshot_collision_matrix_no_holes)


    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')