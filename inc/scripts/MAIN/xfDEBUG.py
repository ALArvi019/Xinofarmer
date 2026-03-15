from http.server import BaseHTTPRequestHandler, HTTPServer
# import urllib.parse
from fish import RunFish
from findImage import RunFindImage


class MyRequestHandler(BaseHTTPRequestHandler):

    def sendOKResponse(self, response):
        # send 200 OK response to client with response
        self.send_response(200)
        # send headers
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        # send response
        self.wfile.write(response.encode('utf-8'))
        return
    

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        datos = post_data.decode("utf-8")
        data = datos.replace('\r', '').replace('\n', '')
        print("Datos recibidos:", data)

        if data == 'XF_2ndScript_Start':
            response = 'XF_2ndScript_Start'
            # print('Send:', response)
            self.sendOKResponse(response)
            return
        command = data.split('|')[0]
        if command and command == 'fromXF':
            # print('Command:', command)
            action = data.split('|')[1]
            # print('Action:', action)
            if action == 'fish':
                src_window = data.split('|')[2]
                images_path = data.split('|')[3]
                fish_type = data.split('|')[4]
                response = RunFish(src_window, images_path, fish_type)
                self.sendOKResponse(response)
                return
            if action == 'findimage':
                src_window = data.split('|')[2]
                images_path = data.split('|')[3]
                image_name = data.split('|')[4]
                response = RunFindImage(src_window, images_path, image_name)
                # print('response:', response)
                self.sendOKResponse(response)
                return

            # if action == 'getcoords':
            #     src_window = data.split('|')[2]
            #     images_path = data.split('|')[3]
            #     image_name = data.split('|')[4]
            #     # remove end of line in image_name
            #     image_name = image_name.replace('\r', '').replace('\n', '')
            #     response = RunFindCoords(src_window, images_path, image_name)
            #     # print('response:', response)
            #     response = response + '@@@@'
            #     conn.send(response.encode('utf-8'))
            # if action == 'findpath':
            #     images_path = data.split('|')[2]
            #     image_name = data.split('|')[3]
            #     start_x = data.split('|')[4]
            #     start_y = data.split('|')[5]
            #     end_x = data.split('|')[6]
            #     end_y = data.split('|')[7]
            #     # remove end of line in end_y
            #     end_y = end_y.replace('\r', '').replace('\n', '')
            #     response = RunFindPath(images_path, image_name, start_x, start_y, end_x, end_y)
            #     # print('response:', response)
            #     response = response + '@@@@'
            #     conn.send(response.encode('utf-8'))
            # if action == 'goto':
            #     src_window = data.split('|')[2]
            #     images_path = data.split('|')[3]
            #     image_name = data.split('|')[4]
            #     end_x = data.split('|')[5]
            #     end_y = data.split('|')[6]
            #     # remove end of line in end_y
            #     end_y = end_y.replace('\r', '').replace('\n', '')
            #     response = RunGoTo(src_window, images_path, image_name, end_x, end_y)
            #     print('response:', response)
            #     response = response + '@@@@'
            #     conn.send(response.encode('utf-8'))
            # if action == 'dungeon':
            #     src_window = data.split('|')[2]
            #     images_path = data.split('|')[3]
            #     image_name = data.split('|')[4]
            #     # remove end of line in end_y
            #     image_name = image_name.replace('\r', '').replace('\n', '')
            #     response = RunDungeon(src_window, images_path, image_name)
            #     print('response:', response)
            #     response = response + '@@@@'
            #     conn.send(response.encode('utf-8'))
        else:
            self.send_error(400, "Unknown command")

    def do_GET(self):
        self.send_error(400, "Not supported")

    def do_PUT(self):
        self.send_error(400, "Not supported")

    def do_DELETE(self):
        self.send_error(400, "Not supported")


if __name__ == '__main__':
    server_address = ('', 9000)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('Listening on port 9000...')
    httpd.serve_forever()
