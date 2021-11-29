import socket
import threading
import http.server


ADDRESS = 'localhost'
TCP_PORT = 7500
UDP_PORT = 8000
HTTP_PORT = 8002


class HttpHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200) #accept
        self.send_header('Content-type', 'text/html')
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
            while True:
                data = self.udp_socket.recvfrom(1024) #tutorials say this is the maximum length of sent data idk
                if data:
                    string_data = data[0].decode(encoding='utf-8')
                    print("Received via UDP:", string_data)
                    if string_data:
                        send_data = Driver.respond(string_data)
                        self.udp_socket.sendto(bytes(send_data, encoding='utf8'), data[1])
                        print("Sent back via UDP:", send_data)

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
                    
    def respond(string) -> str:
        return string + " / (Server response)"




if __name__ == '__main__':
    Driver().startClients()
