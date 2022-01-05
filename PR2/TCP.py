import socket
import threading

IP = 'localhost'
PORT = 7500
BUFFER_SIZE = 1024
LOAD = "TCP Stream "

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))
    sock.listen()
    data = sock.send(bytes(LOAD, encoding='utf8'))
    response = sock.recv(BUFFER_SIZE)

    response_str = response.decode("utf-8")
    print("LOAD sent via TCP:", str(LOAD))
    print("LOAD returned:", response_str)

    ##################################################################################

    clients = []
    nicknames = []

    def broadcast(message):
        for client in clients:
            client.send(message)
    
    def handle(client):
        while True:
            try:
                message = client.recv(1024)
                broadcast(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode('ascii'))
                nicknames.remove(nickname)

    def receive():
        while True:
            client, address = sock.accept()
            print(f"Connected with {str(address)}")
            client.send('Nick'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            print(f'Nickname of the client is {nickname}')
            broadcast(f'{nickname} joined the chat!'.encode('ascii'))
            client.send('Connected to the server'.encode('ascii'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

    print("Server is listening")
    receive()

    sock.close()
