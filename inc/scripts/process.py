# import numpy as np
# import sys
# import cv2

def is_valid_position(img, x, y):
    return x >= 0 and x < img.shape[1] and y >= 0 and y < img.shape[0] and img[y][x] == 0

def bfs(img, start_x, start_y):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    queue = [(start_x, start_y)]
    visited = set()
    while queue:
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid_position(img, new_x, new_y):
                queue.append((new_x, new_y))
                if img[new_y][new_x] == 0:
                    return (new_x - start_x, new_y - start_y)
    return None

# Función para controlar el movimiento del personaje
def move_player(key, player_x, player_y, player_speed, collision_map):
    if key == "w":
        player_y -= player_speed
        if collision_map[player_y, player_x] == 1:
            player_y += player_speed
    if key == "s":
        player_y += player_speed
        if collision_map[player_y, player_x] == 1:
            player_y -= player_speed
    if key == "a":
        player_x -= player_speed
        if collision_map[player_y, player_x] == 1:
            player_x += player_speed
    if key == "d":
        player_x += player_speed
        if collision_map[player_y, player_x] == 1:
            player_x -= player_speed
    return player_x, player_y

def hold_Key (key, hold_time):
    import time, pyautogui
    pyautogui.hold(key)
    time.sleep(hold_time)
    pyautogui.keyUp(key)

# src_file = sys.argv[1]
# dst_file = sys.argv[2]

# img = cv2.imread(src_file)

# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# lower_red = np.array([0,50,50])
# upper_red = np.array([10,255,255])
# lower_yellow = np.array([20,50,50])
# upper_yellow = np.array([30,255,255])
# lower_orange = np.array([10,50,50])
# upper_orange = np.array([20,255,255])

# mask_red = cv2.inRange(hsv, lower_red, upper_red)
# mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
# mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

# mask = cv2.bitwise_or(mask_red, mask_yellow)
# mask = cv2.bitwise_or(mask, mask_orange)

# mask = cv2.bitwise_not(mask)

# img = cv2.bitwise_and(img, img, mask=mask)

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# mean, std = np.mean(gray), np.std(gray)
# low_threshold = int(mean + std) + 61
# high_threshold = low_threshold + 12

# edges = cv2.Canny(gray, low_threshold, high_threshold)

# _, binary = cv2.threshold(edges, 128, 255, cv2.THRESH_BINARY)

# result = bfs(binary, 460, 254)

# if result:
# 	# trnsform to string
# 	result = str(result)
# 	print(result)
# 	# x, y = result
# 	# new_x, new_y = 460 + x, 254 + y
# 	# cv2.circle(img, (460, 254), 5, (0, 0, 255), -1)
# 	# cv2.circle(img, (new_x, new_y), 5, (255, 0, 0), -1)
# else:
# 	print("No se encontró un camino válido")

# # cv2.imshow("Result", img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()





# el personaje se encuentra en la posición 457, 254 de la imagen

# ----------------------------------------------------------------------------------------------------------------------------



































# REAL TIME------------------>
import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from hsvfilter import HsvFilter

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
wincap = WindowCapture('LDPlayer')

hsv_filter = HsvFilter(0, 180, 129, 15, 229, 243, 143, 0, 67, 0)

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # ------------------------------------

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

    # set automatic thresholds using std deviation from mean
    mean, std = np.mean(gray), np.std(gray)
    low_threshold = int(mean + std) + 61
    high_threshold = low_threshold + 12

    edges = cv.Canny(gray, low_threshold, high_threshold)
    # edges = cv.Canny(dilated_image, edge_filter.canny1, edge_filter.canny2)

    _, binary = cv.threshold(edges, 128, 255, cv.THRESH_BINARY)

    collision_matrix = np.zeros_like(binary)
    collision_matrix[binary > 0] = 1

    black_image = np.zeros((collision_matrix.shape[0], collision_matrix.shape[1], 3), dtype=np.uint8)

# Recorrer la matriz de colisión y dibujar rectángulos blancos donde haya paredes
    for i in range(collision_matrix.shape[0]):
        for j in range(collision_matrix.shape[1]):
            if collision_matrix[i, j] == 1:
                cv.rectangle(black_image, (j, i), (j+1, i+1), (255, 255, 255), -1)
	
	# Definir la posición inicial del personaje
    player_x = 83
    player_y = 57

# Definir la velocidad del personaje
    player_speed = 5
	# sleep(1)

    if collision_matrix[player_y - player_speed, player_x] == 0:
        # press "w" key 1 second
        hold_Key("w", 1)
        print("arriba")
        # player_x, player_y = move_player("w", player_x, player_y, player_speed, collision_matrix)
    elif collision_matrix[player_y + player_speed, player_x] == 0:
        hold_Key("s", 1)
        print("abajo")
        # player_x, player_y = move_player("s", player_x, player_y, player_speed, collision_matrix)
    elif collision_matrix[player_y, player_x - player_speed] == 0:
        hold_Key("a", 1)
        print("izquierda")
        # player_x, player_y = move_player("a", player_x, player_y, player_speed, collision_matrix)
    elif collision_matrix[player_y, player_x + player_speed] == 0:
        hold_Key("d", 1)
        print("derecha")
        # player_x, player_y = move_player("d", player_x, player_y, player_speed, collision_matrix)

    # result = bfs(binary, 93, 57)
    # # print(result)
    # # if result is (0, 1) then print "up"
    # # if result is (0, -1) then print "down"
    # # if result is (1, 0) then print "right"
    # # if result is (-1, 0) then print "left"
    # # if result is (-1, -1) then print "down left"
    # # if result is (-1, 1) then print "up left"
    # # if result is (1, -1) then print "down right"
    # # if result is (1, 1) then print "up right"

    # if result:
    #     # trnsform to string
    #     result = str(result)
    #     if result == "(0, 1)":
    #         print("up")
    #     elif result == "(0, -1)":
    #         print("down")
    #     elif result == "(1, 0)":
    #         print("right")
    #     elif result == "(-1, 0)":
    #         print("left")
    #     elif result == "(-1, -1)":
    #         print("down left")
    #     elif result == "(-1, 1)":
    #         print("up left")
    #     elif result == "(1, -1)":
    #         print("down right")
    #     elif result == "(1, 1)":
    #         print("up right")
    # else:
    #     print("No se encontró un camino válido")


    # if image is the same in 5 seconds then sleep 5 seconds and print "No se encontró un camino válido"
    



    cv.imshow('Result', binary)
    cv.imshow('Result2', black_image)

    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')