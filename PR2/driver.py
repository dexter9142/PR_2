import base64
import socket, imutils
import os
import threading
import http.server
import cv2
import numpy as np
import http.server
import cgi
import base64
import json
from urllib.parse import urlparse, parse_qs
import random
import string
import smtp
import webbrowser

from cv2 import CALIB_FIX_TANGENT_DIST

host_name = socket.gethostname()
ADDRESS = socket.gethostbyname(host_name)
TCP_PORT = 7500
UDP_PORT = 8001
HTTP_PORT = 8889


class HttpHandler(http.server.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 'Basic realm="Demo Realm"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        key = self.server.get_auth_key()

        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'No auth header received'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            getvars = self._parse_GET()

            response = {
                'path': self.path,
                'get_vars': str(getvars)
            }
            ########################################################################################Here 
            print("I am here")
            driver = Driver()
 
            driver.afterAuth()
            server.shutdown()
            # Lol did this really work? ahahahahaha

            base_path = urlparse(self.path).path
            if base_path == '/path1':
                pass
            elif base_path == '/path2':
                pass

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        else:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'Invalid credentials'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def do_POST(self):
        key = self.server.get_auth_key()

        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'No auth header received'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            postvars = self._parse_POST()
            getvars = self._parse_GET()

            response = {
                'path': self.path,
                'get_vars': str(getvars),
                'get_vars': str(postvars)
            }

            base_path = urlparse(self.path).path
            if base_path == '/path1':

                pass
            elif base_path == '/path2':

                pass

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        else:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'Invalid credentials'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        response = {
            'path': self.path,
            'get_vars': str(getvars),
            'get_vars': str(postvars)
        }

        self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def _parse_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(
                self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        return postvars

    def _parse_GET(self):
        getvars = parse_qs(urlparse(self.path).query)

        return getvars


class CustomHTTPServer(http.server.HTTPServer):
    key = ''

    def __init__(self, address, handlerClass=HttpHandler):
        super().__init__(address, handlerClass)

    def set_auth(self, username, password):
        self.key = base64.b64encode(
            bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key


class Driver:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((ADDRESS, TCP_PORT))

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((ADDRESS, UDP_PORT))

        self.http_server = http.server.HTTPServer((ADDRESS, HTTP_PORT), HttpHandler)

    

    def startClients(self):

        http_stream = threading.Thread(target=self.startHTTP)
        http_stream.start()
        print("http on")

    def afterAuth(self):
            tcp_stream = threading.Thread(target=self.startTCP)
            udp_stream = threading.Thread(target=self.startUDP)

            protocol = input("1.) Start chat\n2.) Start video stream")

            match protocol:
                case '1':
                    tcp_stream.start()
                    print("tcp on\n")
                    return
                case '2':
                    udp_stream.start()
                    print("udp on\n")
                    return
                case _:
                    print("Wrong")
                    return



    
    
    def startHTTP(self):
        self.http_server.serve_forever()


    def startUDP(self):
       
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        BUFFER_SIZE = 65536
        LOAD = "UDP Stream"

        if __name__ == '__main__':
            port = UDP_PORT
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            print(host_ip)
            socket_address = (host_ip, port)
            sock.bind(socket_address)
            print('Listening at: ', socket_address)


            bytesSent = sock.sendto(bytes(LOAD, encoding='utf8'), (host_ip, port)) #bytes
            response = sock.recvfrom(BUFFER_SIZE)[0]

            response_str = response.decode("utf-8")
            print("LOAD sent via UDP:", str(LOAD))
            print("LOAD sent via UDP:", response_str)


            #cd path
            # run udp, then driver
            vid = cv2.VideoCapture('video.mp4')
            fps,st,frames_to_count, cnt = (0, 0, 20, 0)
            if (vid.isOpened()== False):
                print("Error opening video stream or file")

            while True:
                msg, client_addr = sock.recvfrom(BUFFER_SIZE)
                print('GOT connection from: ', client_addr)
                WIDTH = 400
                while(vid.isOpened()):
                    _, frame = vid.read()
                    frame = imutils.resize(frame, width=WIDTH)
                    encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    message = base64.b64encode(buffer)
                    sock.sendto(message, client_addr)
                    cv2.imshow('TRANSMITING VIDEO', frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        sock.close()
                        break
                

        # sock.close()


    def startTCP(self):
        
        host = "127.0.0.1"
        port = TCP_PORT

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()


        clients = []
        nicknames = []

        def broadcast(message):
            for client in clients:
                client.send(message)

        # Recieving Messages from client then broadcasting
        def handle(client):
            while True:
                try:
                    msg = message = client.recv(1024)  
                    if msg.decode('ascii').startswith('KICK'):
                        if nicknames[clients.index(client)] == 'admin':
                            name_to_kick = msg.decode('ascii')[5:]
                            kick_user(name_to_kick)
                        else:
                            client.send('Command Refused!'.encode('ascii'))
                    elif msg.decode('ascii').startswith('BAN'):
                        if nicknames[clients.index(client)] == 'admin':
                            name_to_ban = msg.decode('ascii')[4:]
                            kick_user(name_to_ban)
                            with open('bans.txt','a') as f:
                                f.write(f'{name_to_ban}\n')
                            print(f'{name_to_ban} was banned by the Admin!')
                        else:
                            client.send('Command Refused!'.encode('ascii'))
                    else:
                        broadcast(message)   # As soon as message recieved, broadcast it.
                
                except:
                    if client in clients:
                        index = clients.index(client)
                        #Index is used to remove client from list after getting diconnected
                        client.remove(client)
                        client.close
                        nickname = nicknames[index]
                        broadcast(f'{nickname} left the Chat!'.encode('ascii'))
                        nicknames.remove(nickname)
                        break
        # Main Recieve method
        def recieve():
            while True:
                client, address = server.accept()
                print(f"Connected with {str(address)}")
                # Ask the clients for Nicknames
                client.send('NICK'.encode('ascii'))
                nickname = client.recv(1024).decode('ascii')
                # If the Client is an Admin promopt for the password.
                with open('bans.txt', 'r') as f:
                    bans = f.readlines()
                
                if nickname+'\n' in bans:
                    client.send('BAN'.encode('ascii'))
                    client.close()
                    continue

                if nickname == 'admin':
                    client.send('PASS'.encode('ascii'))
                    password = client.recv(1024).decode('ascii')
                    # I know it is lame, but my focus is mainly for Chat system and not a Login System
                    if password != 'adminpass':
                        client.send('REFUSE'.encode('ascii'))
                        client.close()
                        continue

                nicknames.append(nickname)
                clients.append(client)

                print(f'Nickname of the client is {nickname}')
                broadcast(f'{nickname} joined the Chat'.encode('ascii'))
                client.send('Connected to the Server!'.encode('ascii'))

                # Handling Multiple Clients Simultaneously
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()

        def kick_user(name):
            if name in nicknames:
                name_index = nicknames.index(name)
                client_to_kick = clients[name_index]
                clients.remove(client_to_kick)
                client_to_kick.send('You Were Kicked from Chat !'.encode('ascii'))
                client_to_kick.close()
                nicknames.remove(name)
                broadcast(f'{name} was kicked from the server!'.encode('ascii'))


        #Calling the main method
        print('Server is Listening ...')
        recieve()
    
                    

def openAuth():
    url = 'http://localhost:8889'
    webbrowser.register('chrome',
    None,
    webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open_new(url)



if __name__ == '__main__':
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    print(password)
    smtp.sendSMTP(password)
    server = CustomHTTPServer(('localhost', HTTP_PORT))
    openAuth()
    server.set_auth('demo', password)

    # response = requests.head("http://localhost:8888")
    # status_code = response.status_code()
    # print(status_code)
 
    server.serve_forever()

   
    Driver().startClients()
    