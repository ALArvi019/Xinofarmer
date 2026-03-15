import pyautogui
import time

w = [1, 0, 0, 0, 0, 0, 0, 0, 0]
s = [0, 1, 0, 0, 0, 0, 0, 0, 0]
a = [0, 0, 1, 0, 0, 0, 0, 0, 0]
d = [0, 0, 0, 1, 0, 0, 0, 0, 0]
wa = [0, 0, 0, 0, 1, 0, 0, 0, 0]
wd = [0, 0, 0, 0, 0, 1, 0, 0, 0]
sa = [0, 0, 0, 0, 0, 0, 1, 0, 0]
sd = [0, 0, 0, 0, 0, 0, 0, 1, 0]
nk = [0, 0, 0, 0, 0, 0, 0, 0, 1]


def keys_to_output(keys, sleep):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    if keys == wa:
        pyautogui.keyDown('w')
        pyautogui.keyDown('a')
        time.sleep(sleep)
        pyautogui.keyUp('w')
        pyautogui.keyUp('a')
    elif keys == wd:
        pyautogui.keyDown('w')
        pyautogui.keyDown('d')
        time.sleep(sleep)
        pyautogui.keyUp('w')
        pyautogui.keyUp('d')
    elif keys == sa:
        pyautogui.keyDown('s')
        pyautogui.keyDown('a')
        time.sleep(sleep)
        pyautogui.keyUp('s')
        pyautogui.keyUp('a')
    elif keys == sd:
        pyautogui.keyDown('s')
        pyautogui.keyDown('d')
        time.sleep(sleep)
        pyautogui.keyUp('s')
        pyautogui.keyUp('d')
    elif keys == w:
        pyautogui.keyDown('w')
        time.sleep(sleep)
        pyautogui.keyUp('w')
    elif keys == s:
        pyautogui.keyDown('s')
        time.sleep(sleep)
        pyautogui.keyUp('s')
    elif keys == a:
        pyautogui.keyDown('a')
        time.sleep(sleep)
        pyautogui.keyUp('a')
    elif keys == d:
        pyautogui.keyDown('d')
        time.sleep(sleep)
        pyautogui.keyUp('d')
    else:
        pyautogui.keyUp('w')
        pyautogui.keyUp('s')
        pyautogui.keyUp('a')
        pyautogui.keyUp('d')
        time.sleep(sleep)


def main():
    # read file registros.txt
    file = open('registros.txt', 'r')
    
    prev_timestamp = None

    # read all lines
    lines = file.readlines()
    # for each line
    for line in lines:
        # split line by |
        line = line.split('|')
        # get keys
        keys = eval(line[0])
        # get timestamp
        timestamp = float(line[1])

        # calculate sleep time
        if prev_timestamp is not None:
            sleep_time = timestamp - prev_timestamp
        else:
            sleep_time = 0

        # update prev_timestamp
        prev_timestamp = timestamp

        # send keys with calculated sleep time
        keys_to_output(keys, sleep_time)

 



if __name__ == '__main__':
    # sleep 3 seconds to start
    time.sleep(3)
    print('STARTING!!!')
    # call main function
    main()
