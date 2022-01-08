import cv2
import imutils, socket
import time
import base64
import numpy as np
import os


host_name = socket.gethostname()
ADDRESS = socket.gethostbyname(host_name)
buffer = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer)
host_name = socket.gethostname()
print(ADDRESS)
port = 8002
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
