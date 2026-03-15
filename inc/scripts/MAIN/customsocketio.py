import threading
import socketio
import time
import subprocess
import requests


class CustomSocketIO(threading.Thread):
    def __init__(self, send_text_to_bot, from_python, mailuser):
        threading.Thread.__init__(self)
        self.stopped = False
        self.is_running = True
        self.paused = False
        self.socketio = None
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.mailuser = mailuser
        try:
            self.uuid_hw = str(subprocess.check_output(
                'wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
        except Exception as e:
            print('aa',e)
            self.uuid_hw = 'error'
        try:
            self.actual_ip_public = self.get_actual_ip_public()
        except Exception as e:
            print('bb',e)
            self.actual_ip_public = 'error'

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True

    def get_actual_ip_public(self):
        try:
            response = requests.get('https://example.com/xf/get-public-ip')  # Configure your domain
            # Verifica si la solicitud HTTP fue exitosa (código de estado 200)
            if response.status_code == 200:
                data = response.json()
                
                # Verifica si la respuesta contiene una clave 'status' con el valor 'success'
                if 'status' in data and data['status'] == 'success':
                    return data['ip']
        except Exception as e:
            print('cc',e)
        return 'error'

    def run(self):
        print('SocketIO thread started')
        while self.socketio is None:
            # if 1 == 1:
            try:
                if self.socketio is None:
                    self.socketio = socketio.Client()
                    self.socketio.connect(
                        'https://node.example.com', wait=True, wait_timeout=10)  # Configure your domain

                @self.socketio.on('connect')
                def on_connect():
                    print('connect')
                    self.socketio.emit(
                        'send_mailuser_to_python', 'connected-' + self.mailuser)

                self.socketio.emit('send_mailuser_to_python',
                                   self.mailuser + '-' + self.uuid_hw)

                self.socketio.emit('check_if_user_is_connected',
                                   self.mailuser + '|' + self.uuid_hw)

                @self.socketio.on('disconnect')
                def on_disconnect():
                    print('disconnect')

                @self.socketio.on('force_disconnect_other_session')
                def on_force_disconnect_other_session(data):
                    print('force_disconnect_other_session...')
                    split_data = data.split('|')
                    mailuser = split_data[0]
                    uuid_hw = split_data[1]
                    ip = split_data[2]
                    if self.mailuser == mailuser and self.actual_ip_public != ip:
                        print('force_disconnect_other_session listo')
                        self.send_text_to_bot.send(
                            'command|exitXFlisto', self.from_python, False, True)

                @self.socketio.on('send_telegram_message_to_python')
                def on_send_telegram_message_to_python(data):
                    self.send_text_to_bot.send(
                        'The screenshot has been successfully sent to telegram', self.from_python, 'green')

            except Exception as e:
                print('SocketIO thread error:', e)

            # check if socketio is connected
            if self.socketio is not None:
                if self.socketio.connected is False:
                    self.socketio = None
                    print('SocketIO disconnected, trying to reconnect')
            time.sleep(5)

    def send(self, thread, data):
        try:
            if self.socketio is not None:
                self.socketio.emit(thread, data)
        except Exception as e:
            print('SocketIO thread error:', e)

    def checkIfConnected(self):
        try:
            if self.socketio is not None:
                return self.socketio.connected
        except Exception as e:
            print('SocketIO thread error:', e)
        return False
