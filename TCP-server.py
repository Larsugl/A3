# A Simple TCP server, used as a warm-up exercise for assignment A3

from socket import *

HOST = "localhost"
PORT = 55555

server_socket = socket(AF_INET, SOCK_STREAM)

def run_server():

    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Starting TCP server...")
    connection_socket, client_address = server_socket.accept()
    while True:
        message = connection_socket.recv(1024).decode()
        print(message)
        if not message:
            break
        if message == "game over":
            break
        try:
            total = sum(map(int, message.split("+")))
            print(total)
            response = str(total)
        except ValueError:
            response = "Not a number"
        connection_socket.sendall(response.encode())
    connection_socket.close()




# Main entrypoint of the script
if __name__ == '__main__':
    run_server()
