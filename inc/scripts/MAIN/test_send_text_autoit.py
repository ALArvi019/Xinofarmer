# import requests

# try:
#     # URL del servidor web de AutoIt
#     url = 'http://127.0.0.1:9001'

#     # Datos a enviar en la solicitud POST
#     data = {'fromxf': 'aaaaa bbbb ccccc ddddd eeeee'}
#     response = requests.post(url, data=data)

#     # Verificar el código de estado de la respuesta
#     if response.status_code == 200:
#         print('Solicitud POST enviada correctamente.')
#     else:
#         print('Error al enviar la solicitud POST.')

# except Exception as e:
#     pass


import cv2 as cv
# path\to\immortal_xinofarmer\inc\img\en\farm\party_invite_en.png
img = cv.imread('path\\to\\immortal_xinofarmer\\inc\\img\\en\\farm\\party_invite_en.png')
cv.imshow('img', img)
cv.waitKey(0)