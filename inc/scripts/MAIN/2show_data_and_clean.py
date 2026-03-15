import numpy as np
import os
import cv2 as cv
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


fileName = "common_models_eval"
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
    

def prepare_training_data(FILE_NAME):

        # carga los datos
        data = np.load('./data/{}/{}-1.npy'.format(FILE_NAME,
                       FILE_NAME), allow_pickle=True)

        # Separar las imágenes y etiquetas
        x = data[:, 0]
        y = data[:, 1]

        # Convertir las imágenes a un array numpy
        x = np.array([i for i in x]).reshape(-1, 110, 173, 1)

        # cv.imshow('test', x[0])
        # cv.waitKey(0)

        # convertir las etiquetas a un array numpy dtype=uint8
        y = np.array([i for i in y])

        print(x.shape)

        # Separar los datos en un conjunto de entrenamiento, validación y prueba
        x_train_val, x_test, y_train_val, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42)
        x_train, x_validate, y_train, y_validate = train_test_split(
            x_train_val, y_train_val, test_size=0.25, random_state=42)  # test_size=0.25 porque 0.2 * 0.8 = 0.16

        x_train = x_train / 255.0
        x_validate = x_validate / 255.0
        x_test = x_test / 255.0

        # mezclar los datos
        indices = np.arange(len(x_train))
        np.random.shuffle(indices)
        x_train = x_train[indices]
        y_train = y_train[indices]

        plt.figure(figsize=(10,10))
        for i in range(100):
            plt.subplot(10,10,i+1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.imshow(x_train[i].reshape(110, 173), cmap=plt.cm.binary)
            plt.xlabel(transform_direction(y_train[i]))
        plt.show()

        print('len(x_train): ', len(x_train))
        print('len(y_train): ', len(y_train))
        print('len(x_validate): ', len(x_validate))
        print('len(y_validate): ', len(y_validate))
        print('len(x_test): ', len(x_test))
        print('len(y_test): ', len(y_test))

        return (x_train, y_train), (x_validate, y_validate), (x_test, y_test)

#prepare_training_data(fileName + '_clean')

if 1 == 1:
    # clean training_data--------------------------
    training_data = []
    while True:
        file_name = './data/' + fileName + '/' + \
            fileName + '-{}.npy'.format(starting_value)
        
        print('LOADING FILE: ', file_name)

        if os.path.isfile(file_name):
            training_data_tmp = np.load(file_name, allow_pickle=True)
            print('training_data_tmp: ', len(training_data_tmp))
            # add training_data_tmp to training_data
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

        # calculate unique hash for img + choice
        hash_value = hash(str(img.tolist()) + str(choice))

        # print unique_data len / training_data len
        print(str(count), '/', len(training_data))

        # check if hash_value is already in unique_data
        if hash_value in unique_data:
            # compare img and choice with those already in unique_data
            for other_data in unique_data[hash_value]:
                if np.array_equal(img, other_data[0]) and np.array_equal(choice, other_data[1]):
                    # if img + choice is equal to another img + choice, then don't add to unique_data
                    break
            else:
                # if img + choice is not equal to any other img + choice with same hash, then add to unique_data
                unique_data[hash_value].append(data)
        else:
            # if hash_value is not in unique_data, then add to unique_data
            unique_data[hash_value] = [data]

    # convert unique_data back to a list of tuples
    training_data = [(data[0], data[1])
                    for data_list in unique_data.values() for data in data_list]

    print('training_data before: ', before)
    print('training_data after: ', len(training_data))

    training_data = np.array(training_data, dtype=object)

    # create folder if not exists
    if not os.path.exists('./data/' + fileName + '_clean'):
        os.makedirs('./data/' + fileName + '_clean' )
    np.save('./data/' + fileName + '_clean' + '/' + fileName + '_clean-1', training_data)

while 1 == 2:
    # show all images in training_data
    for data in training_data:
        img = data[0]
        choice = data[1]
        cv.imshow('test', img)
        # print img resolution
        # save image in folder
        # cv.imwrite('img.png', img)
        # break

        # print(choice)
        if cv.waitKey(25) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break
