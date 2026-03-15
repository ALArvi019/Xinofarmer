from windowcapture import WindowCapture
from preprocess import PreProcessImage
import cv2 as cv
import numpy as np
from getkeys import key_check

wincap = WindowCapture('LDPlayer')
preprocess = PreProcessImage()

hough_thtreshold = 6
hough_minLineLength = 6
hough_maxLineGap = 17

canny_low_threshold = 43
canny_high_threshold = 64
canny_kernel_dimension = 3

player_x = 523
player_y = 340
player_size = 40

resize_multiplier = 6

lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])
lower_yellow = np.array([20, 50, 50])
upper_yellow = np.array([30, 255, 255])
lower_orange = np.array([10, 50, 50])
upper_orange = np.array([20, 255, 255])

thresh_threshold = 149
thresh_walls_threshold = 44
thresh_maxval = 255

dilated_kernel = 9


def get_dilated_contour(contour, contour_dilation=10):
    # Obtener el contorno convexo del contorno original
    hull_contour = cv.convexHull(contour)

    # Definir el tamaño del kernel de dilatación
    kernel = np.ones((contour_dilation, contour_dilation), np.uint8)

    # Convertir el contorno convexo en una máscara binaria
    hull_mask = np.zeros(gray.shape, dtype=np.uint8)
    cv.drawContours(hull_mask, [hull_contour], -1, 255, -1)

    # Aplicar la dilatación a la máscara binaria
    dilated_mask = cv.dilate(hull_mask, kernel)

    # Obtener el contorno dilatado a partir de la máscara binaria
    dilated_contour, _ = cv.findContours(
        dilated_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    dilated_contour = dilated_contour[0]

    return dilated_contour


while True:
    screenshot = wincap.get_screenshot()
    screenshot1 = preprocess.crop(screenshot, 740, 40, 173, 83)

    screenshot1 = cv.resize(screenshot1, (0, 0),
                            fx=resize_multiplier, fy=resize_multiplier)

    gray = cv.cvtColor(screenshot1, cv.COLOR_BGR2GRAY)

    thresh = cv.threshold(gray, thresh_threshold,
                          thresh_maxval, cv.THRESH_BINARY)[1]

    # Encontrar los contornos en la imagen binaria
    contours, hierarchy = cv.findContours(
        thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        original_player_contour = None
        player_contour = None
        for contour in contours:
            if cv.pointPolygonTest(contour, (player_x, player_y), False) == 1:
                original_player_contour = contour
                player_contour = get_dilated_contour(contour, 60)
                player_contour_payer = get_dilated_contour(contour, 20)
                # cv.drawContours(screenshot1, [dilated_contour], -1, (0, 255, 0), 3)
                break

        if player_contour is not None:
            player_center = (player_x, player_y)
            closest_contour = None
            closest_distance = None
            for contour in contours:
                if contour is not original_player_contour:
                    dist = cv.pointPolygonTest(contour, player_center, True)
                    if closest_distance is None or dist > closest_distance:
                        original_closest_contour = contour
                        closest_distance = dist
                        closest_contour = get_dilated_contour(contour, 60)
                        closest_contour_player = get_dilated_contour(contour, 20)
                        # cv.drawContours(screenshot1, [closest_contour], -1, (0, 255, 0), 3)

            if closest_contour is not None and player_contour is not None and closest_contour_player is not None and player_contour_payer is not None:
                # crear una máscara binaria para el contorno del jugador
                player_mask = np.zeros(gray.shape, dtype=np.uint8)
                cv.drawContours(player_mask, [player_contour], -1, 255, -1)

                # crear una máscara binaria para el contorno más cercano
                closest_mask = np.zeros(gray.shape, dtype=np.uint8)
                cv.drawContours(closest_mask, [closest_contour], -1, 255, -1)

                # combinar las máscaras binarias
                mask = cv.bitwise_or(player_mask, closest_mask)

                # encontrar el contorno de la unión de las máscaras
                merged_contour, _ = cv.findContours(
                    mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                
                cv.drawContours(screenshot1, merged_contour, -1, (0, 255, 0), 3)

                # crear una máscara binaria para el contorno del jugador
                player_mask_player = np.zeros(gray.shape, dtype=np.uint8)
                cv.drawContours(player_mask_player, [player_contour_payer], -1, 255, -1)

                # crear una máscara binaria para el contorno más cercano
                closest_mask_player = np.zeros(gray.shape, dtype=np.uint8)
                cv.drawContours(closest_mask_player, [closest_contour_player], -1, 255, -1)

                # combinar las máscaras binarias
                mask_player = cv.bitwise_or(player_mask_player, closest_mask_player)

                # encontrar el contorno de la unión de las máscaras
                merged_contour_player, _ = cv.findContours(
                    mask_player, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                
                cv.drawContours(screenshot1, merged_contour_player, -1, (0, 255, 0), -1)

                edges = cv.Canny(gray, canny_low_threshold,
                                 canny_high_threshold, canny_kernel_dimension)
                kernel = np.ones((dilated_kernel, dilated_kernel), np.uint8)
                dilated_edges = cv.dilate(edges, kernel, iterations=1)

                lines = cv.HoughLinesP(dilated_edges, 1, np.pi / 180, 100,
                                       minLineLength=hough_minLineLength, maxLineGap=hough_maxLineGap)
                if lines is not None:
                    for line in lines:
                        x1, y1, x2, y2 = line[0]
                        x1 = int(x1)
                        y1 = int(y1)
                        x2 = int(x2)
                        y2 = int(y2)
                        # cv.line(screenshot1, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        # if the line is inside merged_contour_player contour, change the color to red
                        if cv.pointPolygonTest(merged_contour[0], (x1, y1), False) == 1 and cv.pointPolygonTest(merged_contour[0], (x2, y2), False) == 1:
                            continue
                        if cv.pointPolygonTest(merged_contour_player[0], (x1, y1), False) == 1 and cv.pointPolygonTest(merged_contour_player[0], (x2, y2), False) == 1:
                            cv.line(screenshot1, (x1, y1), (x2, y2), (0, 0, 255), 2)

                        


                        


                preprocess.image_show('screenshot1', screenshot1, True)
                # preprocess.image_show('mask', mask, True)
                # preprocess.image_show('edges', edges, True)
                preprocess.image_show('dilated_edges', dilated_edges, True)

                # thresh_walls = cv.threshold(gray, thresh_walls_threshold, thresh_maxval, cv.THRESH_BINARY)[1]
                # contours_walls, hierarchy = cv.findContours(thresh_walls, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                # if len(contours_walls) > 0:
                #     contours_to_remove = []
                #     for i, contour in enumerate(contours_walls):
                #         if cv.pointPolygonTest(contour, (player_x, player_y), False) == 1:
                #             contours_to_remove.append(i)
                #     # Eliminar los contornos seleccionados
                #     contours_walls = [c for i, c in enumerate(contours_walls) if i not in contours_to_remove]
                #     # dibujar los contornos actualizados
                #     # cv.drawContours(screenshot1, contours_walls, -1, (255, 0, 0), 5)

                #     # create a mask image that contains the contours_walls
                #     mask = np.zeros(gray.shape, dtype=np.uint8)
                #     cv.drawContours(mask, contours_walls, -1, 255, -1)

                #     edges = cv.Canny(gray, canny_low_threshold, canny_high_threshold, canny_kernel_dimension)

                #     lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=hough_minLineLength, maxLineGap=hough_maxLineGap)
                #     if lines is not None:
                #         for line in lines:
                #             x1, y1, x2, y2 = line[0]
                #             x1 = int(x1)
                #             y1 = int(y1)
                #             x2 = int(x2)
                #             y2 = int(y2)
                #             cv.line(screenshot1, (x1, y1), (x2, y2), (0, 255, 0), 2)
                #             # if player_contour or closest_contour touches the line, then it is a wall, so change the color to red
                #             if cv.pointPolygonTest(player_contour, (x1, y1), False) == 1 or cv.pointPolygonTest(player_contour, (x2, y2), False) == 1:
                #                 cv.line(screenshot1, (x1, y1), (x2, y2), (0, 0, 255), 2)

    if 1 == 2:

        # get the biggest con   tour (if detected)
        if len(contours) > 0:
            # find the biggest area
            player_contour = max(contours, key=cv.contourArea)
            x, y, w, h = cv.boundingRect(player_contour)
            player_center = (player_x, player_y)
            closest_contour = None
            closest_distance = None
            for contour in contours:
                if contour is not player_contour:
                    dist = cv.pointPolygonTest(contour, player_center, True)
                    if closest_distance is None or dist > closest_distance:
                        closest_contour = contour
                        closest_distance = dist

            # check if closest_contour is not None
            if closest_contour is not None:
                # get the centter of the closest contour
                M = cv.moments(closest_contour)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])

                    # binary_image = np.zeros(gray.shape, dtype=np.uint8)
                    merged_contour = np.concatenate(
                        (player_contour, closest_contour))

                    cv.drawContours(
                        screenshot1, [merged_contour], -1, (255, 255, 255), -1)

                    edges = cv.Canny(gray, canny_low_threshold,
                                     canny_high_threshold, canny_kernel_dimension)

                    lines = cv.HoughLinesP(edges, 1, np.pi/180, hough_thtreshold,
                                           minLineLength=hough_minLineLength, maxLineGap=hough_maxLineGap)

                    # if lines is not None:
                    #     for line in lines:
                    #         x1, y1, x2, y2 = line[0]
                    #         x1 = int(x1)
                    #         y1 = int(y1)
                    #         x2 = int(x2)
                    #         y2 = int(y2)

                    #         if cv.pointPolygonTest(player_contours[0], (x1, y1), False) > 0 or cv.pointPolygonTest(player_contours[0], (x2, y2), False) > 0:
                    #             if closest_contour is not None and (cv.pointPolygonTest(closest_contour, (x1, y1), False) > 0 or cv.pointPolygonTest(closest_contour, (x2, y2), False) > 0):
                    #                 # do not draw line if collision with closest contour
                    #                 pass
                    #             elif cv.pointPolygonTest(player_contour, (x1, y1), False) > 0 or cv.pointPolygonTest(player_contour, (x2, y2), False) > 0:
                    #                 # do not draw line if collision with player contour
                    #                 pass
                    #             else:
                    #                 cv.line(screenshot1, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    #                 # print('no collision')
                    #         else:
                    #             cv.line(screenshot1, (x1, y1), (x2, y2), (0, 255, 255), 2)
                    #             # print('collision')

                    preprocess.image_show('Original1', screenshot1, True)
                    preprocess.image_show('Gray', gray, True)
                    preprocess.image_show('Canny', edges, True)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    keys = key_check()
    if 1 == 2:
        if 'A' in keys:
            hough_thtreshold += 1
            print('threshold: ', hough_thtreshold)
            print('minLineLength: ', hough_minLineLength)
            print('maxLineGap: ', hough_maxLineGap)
        if 'Z' in keys:
            hough_thtreshold -= 1
            print('threshold: ', hough_thtreshold)
            print('minLineLength: ', hough_minLineLength)
            print('maxLineGap: ', hough_maxLineGap)
        if 'S' in keys:
            hough_minLineLength += 1
            print('threshold: ', hough_thtreshold)
            print('minLineLength: ', hough_minLineLength)
            print('maxLineGap: ', hough_maxLineGap)
        if 'X' in keys:
            hough_minLineLength -= 1
            print('threshold: ', hough_thtreshold)
            print('minLineLength: ', hough_minLineLength)
            print('maxLineGap: ', hough_maxLineGap)
        if 'D' in keys:
            hough_maxLineGap += 1
            print('threshold: ', hough_thtreshold)
            print('minLineLength: ', hough_minLineLength)
            print('maxLineGap: ', hough_maxLineGap)
        if 'C' in keys:
            hough_maxLineGap -= 1
            print('threshold: ', hough_thtreshold)
            print('minLineLength: ', hough_minLineLength)
            print('maxLineGap: ', hough_maxLineGap)

    if 1 == 2:
        if 'A' in keys:
            canny_low_threshold += 1
            print('low_threshold: ', canny_low_threshold)
            print('high_threshold: ', canny_high_threshold)
            print('kernel_dimension: ', canny_kernel_dimension)
        if 'Z' in keys:
            canny_low_threshold -= 1
            print('low_threshold: ', canny_low_threshold)
            print('high_threshold: ', canny_high_threshold)
            print('kernel_dimension: ', canny_kernel_dimension)
        if 'S' in keys:
            canny_high_threshold += 1
            print('low_threshold: ', canny_low_threshold)
            print('high_threshold: ', canny_high_threshold)
            print('kernel_dimension: ', canny_kernel_dimension)
        if 'X' in keys:
            canny_high_threshold -= 1
            print('low_threshold: ', canny_low_threshold)
            print('high_threshold: ', canny_high_threshold)
            print('kernel_dimension: ', canny_kernel_dimension)
        if 'D' in keys:
            canny_kernel_dimension += 2
            print('low_threshold: ', canny_low_threshold)
            print('high_threshold: ', canny_high_threshold)
            print('kernel_dimension: ', canny_kernel_dimension)
        if 'C' in keys:
            canny_kernel_dimension -= 2
            print('low_threshold: ', canny_low_threshold)
            print('high_threshold: ', canny_high_threshold)
            print('kernel_dimension: ', canny_kernel_dimension)
    if 1 == 2:
        if 'A' in keys:
            thresh_threshold += 1
            print('threshold: ', thresh_threshold)
            print('maxVal: ', thresh_maxval)
        if 'Z' in keys:
            thresh_threshold -= 1
            print('threshold: ', thresh_threshold)
            print('maxVal: ', thresh_maxval)
        if 'S' in keys:
            thresh_maxval += 1
            print('threshold: ', thresh_threshold)
            print('maxVal: ', thresh_maxval)
        if 'X' in keys:
            thresh_maxval -= 1
            print('threshold: ', thresh_threshold)
            print('maxVal: ', thresh_maxval)
    if 1 == 2:
        if 'A' in keys:
            dilated_kernel += 2
            print('dilated_kernel: ', dilated_kernel)
        if 'Z' in keys:
            dilated_kernel -= 2
            print('dilated_kernel: ', dilated_kernel)
