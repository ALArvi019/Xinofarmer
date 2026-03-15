import os
import sys
import numpy as np
import cv2 as cv
from time import time, sleep
from tkinter import simpledialog
import tkinter as tk
from windowcapture import WindowCapture
from preprocess import PreProcessImage
from getkeys import key_check
import pygetwindow as gw
import shutil

# Base path for temporary files
try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.abspath(".")

base_path_tmp = base_path

# Determine the base path
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Path for the 'data' folder
data_folder = os.path.join(base_path, 'data')

# Create the folder if it does not exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Path for the config.txt file
config_path = os.path.join(base_path, 'config.txt')
icon_path = os.path.join(base_path_tmp, 'xf.ico')

# Create the config.txt file if it does not exist
if not os.path.isfile(config_path):
    with open(config_path, 'w') as config_file:
        config_file.write('window_name=\n')
        config_file.write('file_name_prefix=\n')

# Function to save the window name and file name prefix to a config file
def save_config(window_name, file_name_prefix):
    with open(config_path, 'w') as f:
        f.write(f'{window_name}\n')
        f.write(f'{file_name_prefix}\n')

# Function to load the window name and file name prefix from a config file
def load_config():
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                return lines[0], lines[1]
            elif len(lines) == 1:
                return lines[0], ""
    return "", ""

# Initial configuration
minimap_only = True

# Read the window name and file name prefix from the config file
default_window_name, default_file_name_prefix = load_config()

# Create the dialog window using tkinter to ask for the window name
root = tk.Tk()
if os.path.exists(icon_path):
    root.iconbitmap(default=icon_path)
else:
    print("Icon file not found at the specified path.")
root.withdraw()  # Hide the main tkinter window
window_name = simpledialog.askstring("Window Name", "Enter the window name:", initialvalue=default_window_name)

if not window_name:
    print("No window name was entered. Closing the application.")
    exit()

# Check if the window exists
window_list = gw.getWindowsWithTitle(window_name)
if not window_list:
    print(f"Error: No window found with the name '{window_name}'. Closing the application.")
    exit()

# Ask for the file names prefix
file_name_prefix = simpledialog.askstring("File Names", "Enter the prefix for file names:", initialvalue=default_file_name_prefix)

if not file_name_prefix:
    print("No file name prefix was entered. Closing the application.")
    exit()

# Save the configuration to the file
save_config(window_name, file_name_prefix)

# Use data_folder in the rest of the script
file_name_folder = os.path.join(data_folder, file_name_prefix)
if not os.path.exists(file_name_folder):
    os.makedirs(file_name_folder)

starting_value = 1
samples = 0  # Initialize the samples variable with a default value

while True:
    file_name = os.path.join(file_name_folder, f'{file_name_prefix}-{starting_value}.xin')

    if os.path.isfile(file_name):
        print('File exists, moving along', starting_value)
        starting_value += 1
    else:
        print(f'File does not exist, starting from {starting_value}')
        break

def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    w = [1, 0, 0, 0, 0, 0, 0, 0, 0]
    s = [0, 1, 0, 0, 0, 0, 0, 0, 0]
    a = [0, 0, 1, 0, 0, 0, 0, 0, 0]
    d = [0, 0, 0, 1, 0, 0, 0, 0, 0]
    wa = [0, 0, 0, 0, 1, 0, 0, 0, 0]
    wd = [0, 0, 0, 0, 0, 1, 0, 0, 0]
    sa = [0, 0, 0, 0, 0, 0, 1, 0, 0]
    sd = [0, 0, 0, 0, 0, 0, 0, 1, 0]
    nk = [0, 0, 0, 0, 0, 0, 0, 0, 1]

    output = nk
    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'S' in keys and 'A' in keys:
        output = sa
    elif 'S' in keys and 'D' in keys:
        output = sd
    elif 'W' in keys:
        output = w
    elif 'S' in keys:
        output = s
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    return output

def apply_dungeon_mask(screenshot):
    mask = cv.imread('.\dungeon_game_mask.png', cv.IMREAD_UNCHANGED)
    if mask.shape[-1] == 4:
        mask = cv.cvtColor(mask, cv.COLOR_BGRA2GRAY)
    background = np.zeros_like(screenshot)
    background[:, :, 0] = screenshot[:, :, 0]
    background[:, :, 1] = screenshot[:, :, 1]
    background[:, :, 2] = screenshot[:, :, 2]
    screenshot = cv.bitwise_and(background, background, mask=mask)
    return screenshot

def main(file_name, starting_value, samples):
    training_data = []
    for i in list(range(4))[::-1]:
        print(i+1)
        sleep(1)

    wincap = WindowCapture(window_name)
    preprocess = PreProcessImage()

    last_time = time()
    paused = False
    print('STARTING!!!')

    while True:
        if not paused:
            screen = wincap.get_screenshot()
            cv.imwrite('image.png', screen)

            if minimap_only:
                minimap1 = preprocess.crop(screen, 740, 40, 173, 110)
                cv.circle(minimap1, (86, 56), 14, (0, 0, 0), -1)
                rectangle_fix = (39, 82)
                cv.rectangle(minimap1, rectangle_fix, (minimap1.shape[1], minimap1.shape[0]), (0, 0, 0), -1)
            else:
                minimap1 = apply_dungeon_mask(screen)

            minimap = preprocess.to_grayscale(minimap1)
            minimap = cv.resize(minimap, (minimap.shape[1], minimap.shape[0]), interpolation=cv.INTER_AREA)
            minimap = np.expand_dims(minimap, axis=2)
            preprocess.image_show('window', minimap, True, minimap.shape[1], minimap.shape[0])

            keys = key_check()
            output = keys_to_output(keys)

            if output != [0, 0, 0, 0, 0, 0, 0, 0, 1]:  # if not "NOKEY"
                training_data.append([minimap, output])

                if len(training_data) % 100 == 0:
                    print(len(training_data))
                    samples += len(training_data)
                    sleep(1)
                    # if len(training_data) == 300:
                    #     print('SAVING sample: ', samples)
                
                    # Nombre del archivo temporal
                    temp_file_name = os.path.join(base_path_tmp, f'{file_name_prefix}-{starting_value}.npy')
                    
                    # Guardar los datos en el archivo temporal
                    np.save(temp_file_name, np.array(training_data, dtype=object))
                    
                    # Verificar que el archivo se haya guardado completamente
                    while not os.path.isfile(temp_file_name):
                        time.sleep(0.1)
                    
                    print('SAVED. press T for pause')
                    
                    # Nombre del archivo de destino
                    final_file_name = os.path.join(file_name_folder, f'{file_name_prefix}-{starting_value}.xin')
                    
                    # Mover y renombrar el archivo
                    shutil.move(temp_file_name, final_file_name)
                    
                    training_data = []
                    starting_value += 1

        keys = key_check()
        if 'T' in keys:
            paused = not paused
            print('unpaused!' if not paused else 'Pausing!')
            sleep(1)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

print('Done.')
main(file_name, starting_value, samples)
