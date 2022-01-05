import cv2
import imutils, socket
import time
import base64
import numpy as np
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
BUFFER_SIZE = 65536
LOAD = "UDP Stream"

if __name__ == '__main__':
    port = 8000
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
