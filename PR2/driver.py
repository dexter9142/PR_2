import base64
import socket
import threading
import http.server
import cv2
import numpy as np

from cv2 import CALIB_FIX_TANGENT_DIST

host_name = socket.gethostname()
ADDRESS = socket.gethostbyname(host_name)
TCP_PORT = 7500
UDP_PORT = 8001
HTTP_PORT = 8002


class HttpHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200) #accept
        self.end_headers()


    def do_GET(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._set_response()
        response_data = Driver.respond(post_data.decode(encoding='utf-8'))
        self.wfile.write(bytes(response_data, encoding='utf-8'))



class Driver:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((ADDRESS, TCP_PORT))

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((ADDRESS, UDP_PORT))

        self.http_server = http.server.HTTPServer((ADDRESS, HTTP_PORT), HttpHandler)

    

    def startClients(self):
        tcp_stream = threading.Thread(target=self.startTCP)
        udp_stream = threading.Thread(target=self.startUDP)
        http_stream = threading.Thread(target=self.startHTTP)

        tcp_stream.start()
        print("Tcp on")
        udp_stream.start()
        print("udp on")
        http_stream.start()
        print("http on")

    
    
    def startHTTP(self):
        self.http_server.serve_forever()


    def startUDP(self):
        buffer = 65536
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer)
        host_name = socket.gethostname()
        print(ADDRESS)
        port = 8000
        message=b'hello'

        client_socket.sendto(message,(ADDRESS, port))
        fps,st,frames_to_count, cnt = (0, 0, 20, 0)

        while True:
            packet, _ = client_socket.recvfrom(buffer)
            data = base64.b64decode(packet, ' /')
            npdata = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            cv2.imshow("Receiving Video", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break


    def startTCP(self):
        self.tcp_socket.listen()
        while True:
            conn, _ = self.tcp_socket.accept()
            with conn:
                data = conn.recv(1024)
                if data:
                    string_data = data.decode(encoding='utf-8')
                    print("Received via TCP:", string_data)
                    if string_data:
                        send_data = Driver.respond(string_data)
                        conn.sendall(bytes(send_data, encoding='utf8'))
                        print("Sent back via TCP:", send_data)
 
                    
    def respond(string):
        return string + " / (Server response)"




if __name__ == '__main__':
    Driver().startClients()
