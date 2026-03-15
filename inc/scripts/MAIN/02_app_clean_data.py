import numpy as np
import sys
import os
import tkinter as tk
from tkinter import simpledialog
import shutil
import time

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
# Path for the config.txt file
config_path = os.path.join(base_path, 'config.txt')
icon_path = os.path.join(base_path_tmp, 'xf.ico')

# Function to show a dialog for entering file name
def ask_for_file_name():
    default_window_name, default_file_name_prefix = load_config()
    root = tk.Tk()
    if os.path.exists(icon_path):
        root.iconbitmap(default=icon_path)
    else:
        print("Icon file not found at the specified path.")
    root.withdraw()  # Hide the main tkinter window
    file_name = simpledialog.askstring("Input", "Enter the file name (without extension):", initialvalue=default_file_name_prefix)
    root.destroy()  # Close the tkinter window
    return file_name

def load_config():
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                return lines[0], lines[1]
            elif len(lines) == 1:
                return lines[0], ""
    return "", ""

# File name and starting value
fileName = ask_for_file_name()  # Ask user for file name
starting_value = 1

class_names = ['↑', '↓', '←', '→', '↖', '↗', '↙', '↘', 'NK']
w = [1, 0, 0, 0, 0, 0, 0, 0, 0]
s = [0, 1, 0, 0, 0, 0, 0, 0, 0]
a = [0, 0, 1, 0, 0, 0, 0, 0, 0]
d = [0, 0, 0, 1, 0, 0, 0, 0, 0]
wa = [0, 0, 0, 0, 1, 0, 0, 0, 0]
wd = [0, 0, 0, 0, 0, 1, 0, 0, 0]
sa = [0, 0, 0, 0, 0, 0, 1, 0, 0]
sd = [0, 0, 0, 0, 0, 0, 0, 1, 0]
nk = [0, 0, 0, 0, 0, 0, 0, 0, 1]

def transform_direction(movement):
    # transform [0 0 0 1 0 0 0 0 0] to [0, 0, 0, 1, 0, 0, 0, 0, 0]
    movement = movement.tolist()
    if movement == w:
        return '↑'
    elif movement == s:
        return '↓'
    elif movement == a:
        return '←'
    elif movement == d:
        return '→'
    elif movement == wa:
        return '↖'
    elif movement == wd:
        return '↗'
    elif movement == sa:
        return '↙'
    elif movement == sd:
        return '↘'
    elif movement == nk:
        return 'NK'

# Prepare training data
if True:
    # Clean training_data--------------------------
    training_data = []
    while True:
        # file_name = './data/' + fileName + '/' + fileName + '-{}.xin'.format(starting_value)
        file_name = os.path.join(data_folder, fileName, fileName + '-{}.xin'.format(starting_value))

        print('LOADING FILE: ', file_name)

        if os.path.isfile(file_name):
            print('file_name exists, moving along', starting_value)
            training_data_tmp = np.load(file_name, allow_pickle=True)
            print('training_data_tmp: ', len(training_data_tmp))
            # Add training_data_tmp to training_data
            for data in training_data_tmp:
                training_data.append(data)
            print('training_data: ', len(training_data))
            starting_value += 1
        else:
            break

    print('training_data before: ', len(training_data))
    before = len(training_data)

    unique_data = {}
    count = 0

    cont = 1
    for data in training_data:
        img = data[0]
        choice = data[1]
        count += 1

        # Calculate unique hash for img + choice
        hash_value = hash(str(img.tolist()) + str(choice))

        # Print unique_data len / training_data len
        print(str(count), '/', len(training_data))

        # Check if hash_value is already in unique_data
        if hash_value in unique_data:
            # Compare img and choice with those already in unique_data
            for other_data in unique_data[hash_value]:
                if np.array_equal(img, other_data[0]) and np.array_equal(choice, other_data[1]):
                    # If img + choice is equal to another img + choice, then don't add to unique_data
                    break
            else:
                # If img + choice is not equal to any other img + choice with same hash, then add to unique_data
                unique_data[hash_value].append(data)
        else:
            # If hash_value is not in unique_data, then add to unique_data
            unique_data[hash_value] = [data]

    # Convert unique_data back to a list of tuples
    training_data = [(data[0], data[1])
                    for data_list in unique_data.values() for data in data_list]

    print('training_data before: ', before)
    print('training_data after: ', len(training_data))

     # Shuffle data
    np.random.shuffle(training_data)

    # Split data into 90% training, 5% evaluation, and 5% test
    total_len = len(training_data)
    train_end_index = int(total_len * 0.90)
    eval_end_index = train_end_index + int(total_len * 0.05)

    training_set = training_data[:train_end_index]
    eval_set = training_data[train_end_index:eval_end_index]
    test_set = training_data[eval_end_index:]

    # Convert to numpy arrays
    training_set = np.array(training_set, dtype=object)
    eval_set = np.array(eval_set, dtype=object)
    test_set = np.array(test_set, dtype=object)

    # Create folder if not exists
    if not os.path.exists('./data/' + fileName + '_clean'):
        os.makedirs('./data/' + fileName + '_clean')
    # np.save('./data/' + fileName + '_clean' + '/' + fileName + '_clean-1', training_data)
    temp_file_name = os.path.join(base_path_tmp, fileName + '_clean-1.npy')
    np.save(temp_file_name, training_set)
    while not os.path.isfile(temp_file_name):
        time.sleep(0.1)
    final_file_name = os.path.join(data_folder, fileName + '_clean', fileName + '_clean-1.xin')
    shutil.move(temp_file_name, final_file_name)
    print('File saved:', './data/' + fileName + '_clean' + '/' + fileName + '_clean-1.xin')

    temp_file_name = os.path.join(base_path_tmp, fileName + '_eval-1.npy')
    np.save(temp_file_name, eval_set)
    while not os.path.isfile(temp_file_name):
        time.sleep(0.1)
    final_file_name = os.path.join(data_folder, fileName + '_clean', fileName + '_eval-1.xin')
    shutil.move(temp_file_name, final_file_name)
    print('File saved:', './data/' + fileName + '_clean' + '/' + fileName + '_eval-1.xin')

    temp_file_name = os.path.join(base_path_tmp, fileName + '_test-1.npy')
    np.save(temp_file_name, test_set)
    while not os.path.isfile(temp_file_name):
        time.sleep(0.1)
    final_file_name = os.path.join(data_folder, fileName + '_clean', fileName + '_test-1.xin')
    shutil.move(temp_file_name, final_file_name)
    print('File saved:', './data/' + fileName + '_clean' + '/' + fileName + '_test-1.xin')

    print('You can close this window now. and execute the next script.')
    # wait 5 seconds before closing the window
    time.sleep(5)
