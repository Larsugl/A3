#################################################################################
# A Chat Client application. Used in the course IELEx2001 Computer networks, NTNU
#################################################################################

from socket import *
from time import sleep


# --------------------
# Constants
# --------------------
# The states that the application can be in
states = [
    "disconnected",  # Connection to a chat server is not established
    "connected",  # Connected to a chat server, but not authorized (not logged in)
    "authorized"  # Connected and authorized (logged in)
]
TCP_PORT = 1300  # TCP port used for communication
SERVER_HOST = "datakomm.work"  # Set this to either hostname (domain) or IP address of the chat server

# --------------------
# State variables
# --------------------
current_state = "disconnected"  # The current state of the system
must_run = True
client_socket = socket(AF_INET, SOCK_STREAM)


def quit_application():

    global must_run
    must_run = False


def send_command(command, arguments):
    global client_socket

    message = "something"
    if command == "sync":
        message = "async" + "\n"
    elif command == "msg":
        if arguments != "":
            content = arguments
            message = ("msg " + content + "\n")
        else:
            send_message()
    elif command == "privmsg":
        if arguments != None:
            content = arguments
            message = ("privmsg " + content + "\n")
        else:
            send_priv_message()
    elif command == "inbox":
        message = ("inbox" + "\n")
    elif command == "users":
        message = ("users" + "\n")
    elif command == "joke":
        message = ("joke" + "\n")
    elif command == "async":
        message = ("sync" + "\n")
    client_socket.sendall(message.encode())
    pass


def read_one_line(sock):

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


def get_servers_response():


    one_line = read_one_line(client_socket)
    return one_line


def connect_to_server():


    global current_state
    global client_socket

    while current_state == "disconnected":
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((SERVER_HOST, TCP_PORT))
            current_state = "connected"
            send_command("sync", None)
        except error as e:
            current_state = "disconnected"
            while current_state == "disconnected":
                try:
                    client_socket.connect((SERVER_HOST, TCP_PORT))
                    current_state = "connected"
                    send_command("sync", None)
                    print("connection lost, reconnecting")
                except error:
                    sleep(2)
    response = get_servers_response()
    if response == "modeok":
        return response
    else:
        print("CONNECTION NOT IMPLEMENTED!")


def disconnect_from_server():
    global client_socket
    global current_state

    send_command("async", None)
    response = get_servers_response()
    if response == "modeok":
        try:
            client_socket.shutdown(SHUT_RDWR)
            client_socket.close()
            print("server", current_state)
        except error:
            print("unable to close connection")
        current_state = "disconnected"


def server_login():
    global current_state

    username = input("Insert username:")
    message = ("login " + username + "\n")
    client_socket.sendall(message.encode())
    response = get_servers_response()
    if response == "loginok":
        current_state = "authorized"
    elif response == "loginerr username already in use":
        print(response)
        server_login()
    else:
        print(response)
        server_login()
    return None


def send_message():
    arguments = input("Type your message:")
    send_command("msg", arguments)
    response = get_servers_response()
    print(response)


def send_priv_message():
    recipient =input("Recipient: ")
    message = input("Type your message: ")
    arguments = (recipient + " " + message)
    send_command("privmsg", arguments)
    response = get_servers_response()
    print(response)


def read_inbox():
    send_command("inbox", None)
    response = get_servers_response()
    print(response)


def get_users():
    send_command("users", None)
    response = get_servers_response()
    print(response)


def get_joke():
    send_command("joke", None)
    response = get_servers_response()
    print(response)


available_actions = [
    {
        "description": "Connect to a chat server",
        "valid_states": ["disconnected"],
        "function": connect_to_server
    },
    {
        "description": "Disconnect from the server",
        "valid_states": ["connected", "authorized"],
        "function": disconnect_from_server
    },
    {
        "description": "Authorize (log in)",
        "valid_states": ["connected", "authorized"],
        "function": server_login
    },
    {
        "description": "Send a public message",
        "valid_states": ["connected", "authorized"],
        "function": send_message
    },
    {
        "description": "Send a private message",
        "valid_states": ["authorized"],
        "function": send_priv_message
    },
    {
        "description": "Read messages in the inbox",
        "valid_states": ["connected", "authorized"],
        "function": read_inbox
    },
    {
        "description": "See list of users",
        "valid_states": ["connected", "authorized"],
        "function": get_users
    },
    {
        "description": "Get a joke",
        "valid_states": ["connected", "authorized"],
        "function": get_joke
    },
    {
        "description": "Quit the application",
        "valid_states": ["disconnected", "connected", "authorized"],
        "function": quit_application
    },
]


def run_chat_client():
    """ Run the chat client application loop. When this function exists, the application will stop """

    while must_run:
        print_menu()
        action = select_user_action()
        perform_user_action(action)
    print("Thanks for watching. Like and subscribe! 👍")


def print_menu():
    """ Print the menu showing the available options """
    print("==============================================")
    print("What do you want to do now? ")
    print("==============================================")
    print("Available options:")
    i = 1
    for a in available_actions:
        if current_state in a["valid_states"]:
            # Only hint about the action if the current state allows it
            print("  %i) %s" % (i, a["description"]))
        i += 1
    print()


def select_user_action():
    """
    Ask the user to choose and action by entering the index of the action
    :return: The action as an index in available_actions array or None if the input was invalid
    """
    number_of_actions = len(available_actions)
    hint = "Enter the number of your choice (1..%i):" % number_of_actions
    choice = input(hint)
    # Try to convert the input to an integer
    try:
        choice_int = int(choice)
    except ValueError:
        choice_int = -1

    if 1 <= choice_int <= number_of_actions:
        action = choice_int - 1
    else:
        action = None

    return action


def perform_user_action(action_index):
    """
    Perform the desired user action
    :param action_index: The index in available_actions array - the action to take
    :return: Desired state change as a string, None if no state change is needed
    """
    if action_index is not None:
        print()
        action = available_actions[action_index]
        if current_state in action["valid_states"]:
            function_to_run = available_actions[action_index]["function"]
            if function_to_run is not None:
                function_to_run()
            else:
                print("Internal error: NOT IMPLEMENTED (no function assigned for the action)!")
        else:
            print("This function is not allowed in the current system state (%s)" % current_state)
    else:
        print("Invalid input, please choose a valid action")
    print()
    return None



if __name__ == '__main__':
    run_chat_client()
