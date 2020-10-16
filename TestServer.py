# Chat server code #

from socket import *
from threading import Thread
import threading
from time import sleep


server_host = "localhost"
server_port = 55555



server_socket = socket(AF_INET, SOCK_STREAM)
client_id = 0
authenticated = False
mode = "sync"
inbox = []
client = {}
inbox_size = 10

jokes = ["A fire hydrant has H2O on the inside and K9P on the outside",
         "Did you hear about the crook who stole a calendar? He got twelve months",
         "Did you hear about the semi-colon that broke the law? He was given two consecutive sentences",
         "I own the world's worst thesaurus. Not only is it awful, it's awful",
         "Moses had the first tablet that could connect to the cloud"]


class ClientHandler(Thread):

    def __init__(self, client_socket, client_id, client_address, authenticated, inbox):
        Thread.__init__(self)
        self._client_socket = client_socket
        self._client_id = "Anon" + str(client_id)
        self._client_address = client_address
        self._authenticated = authenticated
        self._inbox = inbox
        self.lock = threading.Lock()
        with self.lock:
            client[self._client_id] = client_address


        

    def run(self):
        try:
            print(client)
            message = "something"
            while message != "":
                try:
                    self.handle_incoming_message(self._client_id, message)
                    message = self.read_one_line(self._client_socket)
                    print("%s: %s" % (self._client_id, message))
                except error as e:
                    print("error {0}:{1}".format(e.errno, e.strerror))
                    self._client_socket.close()
        except error as e:
            print("error {0}:{1}".format(e.errno, e.strerror))


    def read_one_line(self, sock):

        newline_received = False
        message = ""
        while not newline_received:
            character = sock.recv(1).decode()
            if character == '\n':
                newline_received = True
            elif character == '\r':
                pass
            else:
                message += character
        return message


    def handle_incoming_message(self,sender,msg):
        global server_socket
        global client_ids
        global sockets
        msg = msg.split()
        if msg[0] == "msg":
            message = msg[1:]
            response = self.broadcast(sender, message)
            print(response)
            self._client_socket.send(response.encode())
        elif msg[0] == "async":
            mode = msg[0]
            response = self.set_mode(mode) + "\n"
            self._client_socket.send(response.encode())
        elif msg[0] == "sync":
            mode = msg[0]
            response = self.set_mode(mode) + "\n"
            self._client_socket.send(response.encode())
        elif msg[0] == "login":
            username = msg[1]
            response = self.login(sender, username) + "\n"
            self._client_socket.send(response.encode())
        elif msg[0] == "users":
            response = get_users() + "\n"
            self._client_socket.send(response.encode())
        elif msg[0] == "inbox":
            user = self._client_socket
            response = self.get_inbox(user)
            self._client_socket.send(response.encode())
        elif msg[0] == "joke":
            response = get_joke()
            self._client_socket.send(response.encode())
        elif msg[0] == "privmsg":
            message = " ".join(msg[2:])
            rec = msg[1]
            response = self.priv_msg(sender, rec, message)
            self._client_socket.send(response.encode())


    def login(self,id, username):
        global client_id
        global authenticated

        is_username_available = True
        if username in client:
            is_username_available = False
        if username.isalnum():
            if is_username_available:
                client[username] = client.pop(id)
                response = "loginok"
                return response
            else:
                response = "loginerr username already in use"
                return response
        else:
            response = "loginerr incorrect username format"
            return response


    def set_mode(self, mode):
        mode = mode
        if mode == "async":
            response = "modeok"
            return response
        elif mode == "sync":
            response = "modeok"
            return response


    def get_inbox(self, user):

        response = "function not yet available\n"
        return response

    def broadcast(self, sender, message):
        global client
        msg = " ".join(message) + "\n"
        if msg != "":
            with self.lock:
                for client[sender] in client:
                    if sender == self._client_address:
                        self._client_socket.sendall(msg.encode())
            response = "msgok\n"
            return response


    def priv_msg(self, sender, rec, message):

        if rec in client:
            reci = client[rec]
            msg = ("%s whispers softly: %s" % (sender, message) + "\n")
            self._client_socket.sendto(msg.encode(), reci)
            res = "msgok\n"
        else:
            res = "msgerr recipient not a client\n"
        return res

def run_server():
    global client_id
    global authent
    global inbox
    server_socket.bind((server_host, server_port))
    server_socket.listen()
    print("Server started on port:" + str(server_port))
    print("Server ready for clients")
    must_run = True
    while must_run:
        client_socket, client_address = server_socket.accept()
        client_id += 1
        handler = ClientHandler(client_socket, client_id, client_address, authenticated, inbox)
        handler.start()
        sleep(10)


def get_users():
    global client
    users = ", ".join(client.keys())
    return users

def get_joke():
    global jokes
    response = random.choice(jokes)
    return response


if __name__ == '__main__':
    run_server()



