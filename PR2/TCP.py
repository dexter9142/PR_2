import socket

IP = '127.0.0.1'
PORT = 7500
BUFFER_SIZE = 1024
LOAD = "TCP Stream "

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORT))

    data = sock.send(bytes(LOAD, encoding='utf8'))
    response = sock.recv(BUFFER_SIZE)

    response_str = response.decode("utf-8")
    print("LOAD sent via TCP:", str(LOAD))
    print("LOAD returned:", response_str)
    sock.close()
