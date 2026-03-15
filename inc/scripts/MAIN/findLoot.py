from windowcapture import WindowCapture
import cv2 as cv
import numpy as np
from getkeys import key_check
import os
from findImage import RunFindImage
import time

# 12, 216, 165, 19, 222, 253
lower_color1 = 12
lower_color2 = 216
lower_color3 = 165
upper_color1 = 19
upper_color2 = 222
upper_color3 = 253

group_threshold = 1
eps = 0.99
num_points = 100

def FindLoot(src_window, img_path,  screenshot_pass = None, images_to_search = None, avoid_images = None, found_colors=['yellow', 'orange', 'blue']):
    # print('FindLoot')
    # print('src_window:', src_window)
    # print('img_path:', img_path)
    # print('screenshot_pass:', screenshot_pass)
    # print('images_to_search:', images_to_search)

    # global lower_color1, lower_color2, lower_color3, upper_color1, upper_color2, upper_color3, group_threshold, eps, num_points

    wincap = WindowCapture(src_window)

    # screenshot_pass = cv.imread('screenshot_show.png')

    if screenshot_pass is None:
        screenshot = wincap.get_screenshot()
    else:
        screenshot = screenshot_pass

    screenshot_show = screenshot.copy()
    screenshot_debug = screenshot.copy()

    mask = cv.imread(img_path + '\..\..\game_items\game_mask.png', cv.IMREAD_UNCHANGED)

    if mask.shape[-1] == 4:
        mask = cv.cvtColor(mask, cv.COLOR_BGRA2GRAY)

    # Crear una imagen de fondo negro sólido con el mismo tamaño que la captura de pantalla
    background = np.zeros_like(screenshot)

    # Copiar los canales RGB de la captura de pantalla a la imagen de fondo
    background[:,:,0] = screenshot[:,:,0]
    background[:,:,1] = screenshot[:,:,1]
    background[:,:,2] = screenshot[:,:,2]

    # Aplicar la máscara en la imagen de fondo
    screenshot = cv.bitwise_and(background, background, mask=mask)

    # save screenshot in file test.png
    # cv.imwrite('screenshot_show.png', screenshot_show)
    # return

    screenshot_hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)

    # colors = {
    #     # lower_color1, lower_color2, lower_color3, upper_color1, upper_color2, upper_color3, group_threshold, eps, num_points
    #     'yellow': (30, 167, 40, 36, 173, 245, 1, 0.65),  # GOLD
    #     'orange': (12, 216, 165, 19, 222, 253, 1, 1.19),  # ORANGE
    #     'blue': (118, 152, 26, 121, 161, 244, 1, 0.99),  # BLUE
    # }

    colors = {}
    # foreach found_colors
    for color in found_colors:
        if color == 'yellow':
            colors['yellow'] = (30, 167, 40, 36, 173, 245, 1, 0.65)
        elif color == 'orange':
            colors['orange'] = (12, 216, 165, 19, 222, 253, 1, 1.19)
        elif color == 'blue':
            colors['blue'] = (118, 152, 26, 121, 161, 244, 1, 0.99)
    

    positions_of_loot = {}

    # Buscar los colores
    if colors is not None:
        for color in colors:
            lower = np.array([colors[color][0], colors[color][1], colors[color][2]])
            upper = np.array([colors[color][3], colors[color][4], colors[color][5]])
            # lower = np.array([lower_color1, lower_color2, lower_color3])
            # upper = np.array([upper_color1, upper_color2, upper_color3])

            mask = cv.inRange(screenshot_hsv, lower, upper)
            count = cv.countNonZero(mask)

            if count > num_points:
                # detected_output = cv.bitwise_and(screenshot, screenshot, mask=mask)

                contours, hierarchy = cv.findContours(
                    mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                
                # draw contours in detected_output
                # cv.drawContours(detected_output, contours, -1, (0, 255, 0), 3)

                # obtener la posición del rectángulo que se encuentre mas a la derecha una vez agrupados
                rects = [cv.boundingRect(cnt) for cnt in contours]
                groups = cv.groupRectangles(rects, colors[color][6], colors[color][7])

                # Dibujar los contornos solo si hay suficientes objetos cercanos
                if len(groups[0]) > 1:
                    # print rectangles grouped
                    for rect in groups[0]:
                        # if dont exist positions_of_loot[color], create it
                        if color not in positions_of_loot:
                            positions_of_loot[color] = []
                        positions_of_loot[color].append((rect[0], rect[1]))
                        # x, y, w, h = rect
                        # if color == 'yellow':
                        #     # print circle
                        #     cv.circle(screenshot_debug, (x+w//2, y+h//2),
                        #                 5, (0, 255, 255), -1)
                        # elif color == 'orange':
                        #     cv.circle(screenshot_debug, (x+w//2, y+h//2),
                        #                 5, (0, 165, 255), -1)
                        # elif color == 'blue':
                        #     cv.circle(screenshot_debug, (x+w//2, y+h//2),
                        #                 5, (255, 0, 0), -1)
                        # cv.circle(detected_output, (x+w//2, y+h//2),
                        #                 5, (255, 255, 255), -1)
                        
                    # draw miliseconds on screen
                # cv.putText(detected_output, str(int(time.time()*1000)),
                #            (0, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # Mostrar la imagen con la equis dibujada
                # cv.imshow('Computer Vision2', detected_output)

    if images_to_search is None:
        # read all names of images from folder img_path and save in images_to_search
        images_to_search = ()
        for filename in os.listdir(img_path):
            if filename.endswith(".png"):
                if avoid_images is not None:
                    search_image = True
                    for avoid_image in avoid_images:
                        if avoid_image in filename:
                            search_image = False
                            break
                    if search_image:
                        images_to_search += (filename[:-4],)
                else:
                    images_to_search += (filename[:-4],)

    # find images
    response = RunFindImage(src_window, img_path, images_to_search, screenshot_show, 0.8, False)
    for image in response:
        if response[image] != 'notfound':
            if image not in positions_of_loot:
                positions_of_loot[image] = []
            loot = response[image].split('|')
            positions_of_loot[image].append((int(loot[0]), int(loot[1])))

    # if positions_of_loot:
    #     # print(positions_of_loot)
    #     # draw in screenshot_show the positions of loot
    #     for loot in positions_of_loot:
    #         for position in positions_of_loot[loot]:
    #             cv.circle(screenshot_debug, position, 5, (0, 255, 0), -1)
    #             # and print the name of loot
    #             cv.putText(screenshot_debug, loot, position,
    #                         cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

    # cv.imshow('LOOT screenshot_debug', screenshot_debug)
    # cv.waitKey(1)

    # if positions_of_loot is not {} empty
    if positions_of_loot:
        # pass
        # print(positions_of_loot)
        return positions_of_loot
    else:
        return {'notfound': 'notfound'}
        # pass

    

    # keys = key_check()
    # if 1 == 2:
    #     if 'A' in keys:
    #         lower_color1 += 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'Z' in keys:
    #         lower_color1 -= 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'S' in keys:
    #         lower_color2 += 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'X' in keys:
    #         lower_color2 -= 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'D' in keys:
    #         lower_color3 += 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'C' in keys:
    #         lower_color3 -= 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'F' in keys:
    #         upper_color1 += 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'V' in keys:
    #         upper_color1 -= 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'G' in keys:
    #         upper_color2 += 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'B' in keys:
    #         upper_color2 -= 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'H' in keys:
    #         upper_color3 += 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'N' in keys:
    #         upper_color3 -= 1
    #         print("lower_color1: ", lower_color1, "lower_color2: ", lower_color2, "lower_color3: ", lower_color3,
    #               "upper_color1: ", upper_color1, "upper_color2: ", upper_color2, "upper_color3: ", upper_color3)
    #     if 'Q' in keys:
    #         group_threshold += 1
    #         print("group_threshold: ", group_threshold)
    #     if 'W' in keys:
    #         group_threshold -= 1
    #         print("group_threshold: ", group_threshold)
    #     if 'E' in keys:
    #         eps += 0.1
    #         print("eps: ", eps)
    #     if 'R' in keys:
    #         eps -= 0.1
    #         print("eps: ", eps)



# while True:
#     FindLoot("LDPlayer", "path\\to\\immortal_xinofarmer\\inc\\img\\en\\loot_items", None, None)