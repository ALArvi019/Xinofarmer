import cv2 as cv
import numpy as np


class ProcessImage:

	def __init__(self) -> None:	
		pass

	def delete_colors(self, screenshot):
		# delete colors from the image
		hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
		lower_red = np.array([0,50,50])
		upper_red = np.array([10,255,255])
		lower_yellow = np.array([20,50,50])
		upper_yellow = np.array([30,255,255])
		lower_orange = np.array([10,50,50])
		upper_orange = np.array([20,255,255])

		mask_red = cv.inRange(hsv, lower_red, upper_red)
		mask_yellow = cv.inRange(hsv, lower_yellow, upper_yellow)
		mask_orange = cv.inRange(hsv, lower_orange, upper_orange)

		mask = cv.bitwise_or(mask_red, mask_yellow)
		mask = cv.bitwise_or(mask, mask_orange)

		mask = cv.bitwise_not(mask)

		screenshot = cv.bitwise_and(screenshot, screenshot, mask=mask)

		gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)

		return gray

	def toBynary(self, gray):
		# set automatic thresholds using std deviation from mean
		mean, std = np.mean(gray), np.std(gray)
		low_threshold = int(mean + std) + 61
		high_threshold = low_threshold + 12

		edges = cv.Canny(gray, low_threshold, high_threshold)
		# edges = cv.Canny(dilated_image, edge_filter.canny1, edge_filter.canny2)

		_, binary = cv.threshold(edges, 128, 255, cv.THRESH_BINARY)

		return binary

	def get_collision_matrix(self, binary):
		collision_matrix =  np.array(binary, dtype=int) / 255

		return collision_matrix

	def draw_collision_matrix(self, collision_matrix):
		screenshot = np.zeros((collision_matrix.shape[0], collision_matrix.shape[1], 3), dtype=np.uint8)
		# draw collision matrix
		for i in range(collision_matrix.shape[0]):
			for j in range(collision_matrix.shape[1]):
				if collision_matrix[i][j] == 1:
					# // draw white square 
					screenshot[i][j] = [255, 255, 255]
				else:
					# // draw black square 
					screenshot[i][j] = [0, 0, 0]

		return screenshot
	
	def fill_holes(self, collision_matrix, canny):
		# Define el tamaño y forma del elemento estructurante
		kernel = cv.getStructuringElement(cv.MORPH_RECT, (2,2))

		# Aplica la dilatación a la imagen
		dilation = cv.dilate(canny, kernel, iterations=1)

		# Actualiza la matriz de colisión con la información de la dilatación
		collision_matrix[dilation == 255] = 1

		return collision_matrix



	def delete_image_content(self, img, x1, y1, x2, y2):
		h, w = img.shape[:2]

		if x1 >= 0 and y1 >= 0 and x2 >= 0 and y2 >= 0 and x1 < w and y1 < h and x2 < w and y2 < h:
			# delete image content
			mask = np.zeros((h, w), np.uint8)
			bgdModel = np.zeros((1,65),np.float64)
			fgdModel = np.zeros((1,65),np.float64)
			rect = (x1, y1, x2, y2)
			# draw rect before grabcut and show it
			
			cv.imshow('img1', img)
			cv.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
			cv.imshow('img2', img)
			mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
			cv.imshow('img3', img)
			img = img * mask[:, :, np.newaxis]
			cv.imshow('img4', img)
			dst = cv.inpaint(img, mask, 3, cv.INPAINT_TELEA)
			cv.imshow('img5', dst)
			cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
			return dst
		else:
			return img


