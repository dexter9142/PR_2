import http.client

IP = 'localhost'
PORT = 8002
BUFFER_SIZE = 1024
MESSAGE = "HTTP Stream "
ADDRESS = IP + ":" + str(PORT)

if __name__ == '__main__':
    httpConnection = http.client.HTTPConnection(IP, PORT)
    httpConnection.request("GET", ADDRESS, bytes(MESSAGE, encoding='utf8'))
    response = httpConnection.getresponse()

    response_str = response.read().decode("utf-8")
    print("Message sent via HTTP:", str(MESSAGE))
    print("Message returned:", response_str)
    httpConnection.close()
