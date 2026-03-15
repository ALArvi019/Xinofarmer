import cv2 as cv
import numpy as np

class PreProcessImage:
	def __init__(self):
		pass

	def resize(self, image, width, height):
		return cv.resize(image, (width, height))

	def to_grayscale(self, image):
		return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

	def to_canny(self, image, low_threshold, high_threshold, kernel_dimension):
		return cv.Canny(image, low_threshold, high_threshold, kernel_dimension)
	
	def get_lines(self, image, hough_thtreshold, hough_minLineLength, hough_maxLineGap):
		return cv.HoughLinesP(image, 1, np.pi/180, hough_thtreshold, minLineLength=hough_minLineLength, maxLineGap=hough_maxLineGap)

	def draw_lines(self, image, lines, color, thickness):
		if lines is not None:
			for line in lines:
				for x1,y1,x2,y2 in line:
					cv.line(image, (x1, y1), (x2, y2), color, thickness)

	def print_player_position(self, image, x, y, radius, color, thickness):
		cv.circle(image, (x, y), radius, color, thickness)

	def draw_coliision_between_player_and_lines(self, image, lines, x, y, radius, color, thickness):
		if lines is not None:
			for line in lines:
				x1, y1, x2, y2 = line[0]
				if (x1 - x)**2 + (y1 - y)**2 <= radius**2:
					cv.line(image, (x1, y1), (x2, y2), color, thickness)
				if (x2 - x)**2 + (y2 - y)**2 <= radius**2:
					cv.line(image, (x1, y1), (x2, y2), color, thickness)

	def image_show(self, window_name, image):
		cv.namedWindow(window_name, cv.WINDOW_NORMAL)
		cv.resizeWindow(window_name, 344, 166)
		cv.imshow(window_name, image)

	def image_for_training(self, image):
		image = cv.resize(image, (80, 80))
		image = np.expand_dims(image, axis=0)
		return image
