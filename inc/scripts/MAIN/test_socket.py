import socketio
import time
from windowcapture import WindowCapture
import cv2 as cv
import numpy as np
import base64


socketio = socketio.Client()
socketio.connect('http://localhost:3000', wait=True, wait_timeout=10)


@socketio.on('connect')
def on_connect():
    print('connect')


@socketio.on('disconnect')
def on_disconnect():
    print('disconnect')


@socketio.on('send_telegram_message_to_python')
def on_send_telegram_message_to_python(data):
    print('on_send_telegram_message_to_python', data)


for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

wincap = WindowCapture('LDPlayer')
screenshot = wincap.get_screenshot()
cv.imshow('detected_output', screenshot)


_, compressed_image = cv.imencode('.jpg', screenshot)
base64_image = base64.b64encode(compressed_image).decode('utf-8')

socketio.emit('send_telegram_message', {'image': base64_image, 'username': 'LDPlayer'})




cv.waitKey(1)
exit()

