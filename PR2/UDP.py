import socket

IP = '127.0.0.1'
PORT = 8000
BUFFER_SIZE = 1024
LOAD = "UDP Stream"

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    bytesSent = sock.sendto(bytes(LOAD, encoding='utf8'), (IP, PORT)) #bytes
    response = sock.recvfrom(BUFFER_SIZE)[0]

    response_str = response.decode("utf-8")
    print("LOAD sent via UDP:", str(LOAD))
    print("LOAD sent via UDP:", response_str)
    sock.close()
