# A Simple TCP client, used as a warm-up exercise for socket programming assignment.
# Course IELEx2001, NTNU

import random
import time
from socket import *


from socket import socket

HOST = "localhost"
PORT = 55555

client_socket: socket = socket(AF_INET, SOCK_STREAM)


def connect_to_server(HOST, PORT):


    global client_socket
    try:
        client_socket.connect((HOST, PORT))
    except IOError:
        return False
    else:
        return True


def close_connection():
    """
    Close the TCP connection to the remote server.
    :return: True on success, false otherwise
    """

    global client_socket
    try:
        client_socket.close()
    except IOError:
        return False
    else:
        return True

def send_request_to_server(request):
    """
    :param request: The request message to send. Do NOT include the newline in the message!
    :return: True when message successfully sent, false on error.
    """

    global client_socket
    try:
        message = request
        if not message.upper() != "GAME OVER":
            close_connection()
        else:
            message_encode = message.encode()
            try:
                client_socket.sendall(message_encode)
            except error:
                return False
    except ValueError:
        return False
    else:
        return True


def num_there(s):
    return any(i.isdigit() for i in s)


def read_response_from_server():
    """
    Wait for one response from the remote server.
    :return: The response received from the server, None on error. The newline character is stripped away
     (not included in the returned value).
    """

    global client_socket
    try:
        response = client_socket.recv(1024).decode()
        num_there(response)
        return response
    except IOError:
        return None


def run_client_tests():
    """
    Runs different "test scenarios" from the TCP client side
    :return: String message that represents the result of the operation
    """
    print("Simple TCP client started")
    if not connect_to_server(HOST, PORT):
        return "ERROR: Failed to connect to the server"

    print("Connection to the server established")
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    request = str(a) + "+" + str(b)

    if not send_request_to_server(request):
        return "ERROR: Failed to send valid message to server!"

    print("Sent ", request, " to server")
    response = read_response_from_server()
    if response is None:
        return "ERROR: Failed to receive server's response!"

    print("Server responded with: ", response)
    seconds_to_sleep = 2 + random.randint(0, 5)
    print("Sleeping %i seconds to allow simulate long client-server connection..." % seconds_to_sleep)
    time.sleep(seconds_to_sleep)

    request = "bla+bla"
    if not send_request_to_server(request):
        return "ERROR: Failed to send invalid message to server!"

    print("Sent " + request + " to server")
    response = read_response_from_server()
    if response is None:
        return "ERROR: Failed to receive server's response!"

    print("Server responded with: ", response)
    if not (send_request_to_server("game over") and close_connection()):
        return "ERROR: Could not finish the conversation with the server"

    print("Game over, connection closed")
    if send_request_to_server("2+2"):
        return "ERROR: sending a message after closing the connection did not fail!"

    print("Sending another message after closing the connection failed as expected")
    return "Simple TCP client finished"


# Main entrypoint of the script
if __name__ == '__main__':
    result = run_client_tests()
    print(result)
