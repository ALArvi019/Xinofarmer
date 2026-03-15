import requests

class SendTextToBot:
    def __init__(self):
        pass

    def send(self, text, fromPython=False, color=False, command=False):
        if fromPython:
            print(text)
            return
        try:
            # URL del servidor web de AutoIt
            url = 'http://127.0.0.1:9001'

            if command:
                data = {'fromxf': text}
            else:
                if color:
                    data = {'fromxf': 'color|' + color + '|' + text}
                else:
                    data = {'fromxf': 'color|False|' + text}
            # Datos a enviar en la solicitud POST
            
            response = requests.post(url, data=data, timeout=0.5)

            # Verificar el código de estado de la respuesta
            # if response.status_code == 200:
            #     print('Solicitud POST enviada correctamente.')
            # else:
            #     print('Error al enviar la solicitud POST.')

        except Exception as e:
            pass