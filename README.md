# A3
Assignment to learn how to program networking apps using TCP sockets.
Assignment A3: TCP Socket programming
Autumn 2020
In this assignment, you will learn how to program networking apps using TCP sockets.
Assignment consists of several parts. Some parts are mandatory, some are optional - for more exploration and challenge. 
It is highly recommended that you read all the mandatory parts of the document (OK to skip the optional parts) before you start doing anything else! It will make the picture clear and save a lot of confusion for you!
Table of contents
Team	2
Template code and GIT workflow	2
Requirements and presentation	2
General project description	2
Supporting tools	3
Part 1: Warm-up	3
Template code	4
Simple TCP client	4
Simple TCP Server	6
Debug in wireshark	6
Part 2: Server-client chat	6
Mandatory tasks: TCP chat client	6
Setup	7
Step 1: Connect to chat server	7
Step 2: Implement disconnect	7
Step 3: Switch to synchronous mode	7
Step 4: Wait for server to accept synchronous mode	8
Step 5: Login	8
Step 6:  Send a public message to server	8
Step 7: List users - undocumented feature	8
Step 8: Send a private message	9
Step 9: Print the contents of the inbox	9
Optional tasks: additional features for the chat client	9
Joke command	9
Optional tasks: implement your own chat server	9
Suggested steps	10
Optional tasks: extra challenges for chat server	11
Random joke	11
Filter out spam	11
Team
Part of this exercise is to learn communication and synchronization of code between developers. The projects will be developed in teams. While there are no strict rules on who is typing the code on the keyboard, each developer in the team must understand what is going on in the code and should be able to explain it to the teacher when asked. 
While it is enough to show a single solution for the whole team, it is also OK if every team member wants to develop their own unique solution, with the goal to learn and understand better.
Template code
Template code for this assignment is available in this GIT repository. You won’t have write access to it, create a fork (a copy) of it and work on your own repository.  Or simply download the code as a ZIP file.
Requirements and presentation
Implement the mandatory part. 
Hand in either URL to Git repository or a ZIP file with source code on Blackboard. Make it a group hand-in for all the group members. If some group members have not participated in the development of the project, this must be noted in the comment field of the hand-in.
(For students in Ålesund) Show a demo to the teacher during one of Labs. All team members must show a demo. I.e., either all the group members are present during a single demo, or each of them shows a separate demo. Teacher will ask questions about the code and all group members must understand the code to get it approved. Assignment will be approved individually.
Each student should be able to explain all the steps implemented. It is not acceptable to say “I did not write this part, I don’t understand it”.
It is suggested to write the code in Python. However, you can use any language you like (Java, C++, Golang, …), as long as you understand what you write. If you choose another language, the teachers may not be able to help as much (but will try :)).
The teachers may not approve a messy code which is not readable.
General project description
All the tasks in this assignment are related to building parts of a chat system. A chat server is listening for client connections. Each TCP client represents one chat user. Each user can send and receive messages to and from other users.  All the communication is done through a server. I.e., users don’t send messages directly to each other. Rather, there is a chat server - users send messages to the server, the server forwards messages to necessary recipients.
First, we start with a warm-up exercise. During it you will build understanding and skills that will make it easier to understand the basics of socket programming. 
In the mandatory part you will implement a chat client application with a text-based interface. The client connects to a chat server. All the users connected to the same chat server can chat with each other in one of two ways: a public message sent to everyone; or a private message for a single user.
There is a predefined chat protocol, described in a separate protocol document. Your application must follow the protocol very strictly! It must be able to participate in the chat with other chat clients and servers. The exact code you write is not that important. For example, you can have different names for variables. But the protocol must be followed letter by letter. Otherwise, the chat won’t work.
Note: the newline character \n mentioned in many places below is representing a newline character with ASCII code 10. When you use stream functions which add the newline automatically, make sure you don’t send a double newline!
Supporting tools
To help you with the development, several tools are provided:
A chat server is running at the host datakomm.work, TCP port 1300. You can connect to the server for testing. Or for having fun with other students who will connect at the same server. Warning: no vandalism, harassment, etc!
We provide a precompiled Chat client tool. You can use it to test the whole chat ecosystem: if you implement a chat client, you can connect to the same server; if you make your own chat server, the chat client can be used for tests as well. You can download the latest chat client here. The client uses Microsoft .Net runtime, made for Windows. Instructions on how to run the chat client on Mac or Linux are here. An alternative solution: use this .JAR file, it contains a complete Chat client application, made in Java. It should run on all platforms. 
A template code for the chat client, containing a complete Textual User Interface (TUI) and skeleton for business logic functions. You will get the template code in the GIT repository that you will start with.
You may need to use Wireshark to sniff network packets and find out some undocumented protocol features. We provide a tutorial on how to reverse-engineer protocol using existing client and server applications.
Part 1: Warm-up
In this part you will develop a simple TCP client and TCP server applications. The goal is to get familiar with basic concepts of TCP socket programming. Once you have mastered the basic building blocks (connect, send messages, receive messages, close connection) you can write virtually any network communication application using these blocks.
Before starting programming on your own, take a look at the videos for week 6. Look at the provided examples, identify the basic primitives of every TCP application. Use Wireshark and trace the application in debug mode if you want to understand what is really sent over the network in every step. 
The primitives (or building blocks) of TCP application are a s follows:
Setting up the connection between the client and the server. Notice the difference on the server and the client. What does the server do to accept a new connection? What does the client do? When you see the code - how do you know whether that is a server or a client? 
Sending and receiving messages. How does that happen? 
Closing the connection. 
Once you understand the basic primitives, implement the following applications (a single project, two separate files - one representing a client (the first application) and one representing a server (the second app)). 
Template code
Use project “Warmup-Python” as a template from this GIT repository.
Simple TCP client
First part of the warm-up is creation of a TCP client application. The protocol is as follows:
TCP port 1301 is used for communication
The message exchange is always synchronous and started on the client side. I.e., the client is the first to send a request message. 
The server always takes one request from the client and responds with a single response message. 
The request message has the following format: <number1>+<number2>\n
<number1> and <number2> are two positive integer numbers
+ is the plus sign, ASCII code 43 (‘+’ in program code).
\n is the newline character. 
The response is a string followed by the newline \n. The string depends on the request:
If the request was correct, the server responds with the result of the equation that the client sent (sum of the two numbers).
If there are some errors in the message, then the response is “error”.
The request->response cycle is repeated until the client sends a message “game over\n” to the server. Both the server and the client then terminate the connection without any further message exchange.
Here is a diagram showing an example server-client session: 

The task - implement the TCP client (file simple_tcp_client.py), including functions:
connect_to_server
send_request_to_server
read_response_from_server
close_connection

To test your client, you can connect to an existing server:
Host: datakomm.work
Port: 1301
Simple TCP Server 
Now that you have the client ready, time to implement the server part. The server must follow the same protocol. The task - implement the server part, in file simple_tcp_server.py. While the TCP client had all the logic predefined, in the server the exercise is more open - you should implement everything in the server, including the logic. To make the server usable, use multi-threading - handle each client in a separate CPU thread to allow multiple parallel client connections.
Congratulations! You now have a set of applications that can talk to each other! You could run the server anywhere in the world with Internet connection, for example, in New Zealand. You can run the client anywhere, for example, here in Norway. And they can talk to each other! Magic!
“Any sufficiently advanced technology is indistinguishable from magic.” -- Arthur C. Clarke
Debug in wireshark
You have used the Wireshark tool in the first two assignments. But did you really understand what you were looking at? :)
Now, when you have your own TCP client and server, you can observe what is going on. Launch Wireshark, start recording the packets, then start your TCP client and make it send a packet to the remote server (hostname: datakomm.work, port 1301). Then go to wireshark and find out the following (no instruction given, try to figure it out on your own, it will be good practice):
Set up a filter to see only packets belonging to the warmup application (packets sent and received by the warmup TCP client). 
Observe the packets. How many packets are there? Try to understand the meaning of each packet (opening a connection, sending data, receiving data, closing connection).
Where can you see the IP address of the remote server?
Where can you see which TCP port on the server was used?
Where can you see which local TCP port your client application used (it will not be 1301)?
This concludes the warm-up stage. Now you are familiar with all the necessary concepts and are ready to build a chat application.
Part 2: Server-client chat
In this part you will build a chat application. It consists of two parts:
The client side (TCP client). It connects to a server. This part is mandatory.
The server side - a TCP server that runs on a host, accepts incoming connections from clients and communicates with them using the protocol described below. This part is optional.
Read the Chat protocol document before you continue! It describes protocol for both the server and the client. 
Mandatory tasks: TCP chat client
Your task in this part is to program a Chat client that uses TCP socket communication. The client connects to a chat server, can send and receive chat messages.
For testing, we provide a chat server. It is available at host datakomm.work, TCP port 1300. You can connect your client to it for testing.
A template is available in this GIT repository, ChatClient-Python folder. It contains code for printing out the menu of available options. You need to fill in code related to socket communication and logic based on the chat protocol. 
You should use the synchronous mode - messages from the server can come only as a response to a request from the client. While you can choose to implement the asynchronous mode also, it would be more challenging and will require two threads: one for reading user input and reacting on it (sending requests to the server) and one for reacting on incoming commands from the server. Try the synchronous mode first. When it is working, you can extend the application to asynchronous mode. Read the protocol documentation on how to switch to the synchronous mode.
Read the provided template carefully before writing any code on your own! There are many pieces of code which can save you time and avoid writing things from scratch. This approach is typical in real industrial projects as well. You rarely write something from scratch. Reading existing code is an important skill. 
Setup
You should continue to work on the template code you got from the GIT repository. Open the project in PyCharm (or any other Python editor of your choice (note: Jupyter notebook may not work properly)). You will see a runnable application. Try to understand the meaning of the different functions and variables. Then follow the instructions below and look for “TODO - Step X” places in the code. In some cases you will need to also create new functions.
Step 1: Connect to chat server
The first step is to implement connection to the chat server. 
Implement function connect_to_server(). It should establish a connection to a chat server.The host and TCP port are stored in constants SERVER_HOST and TCP_PORT. Use those. It should also change the variable current_state to “connected” if the connection was successful. Remember to handle the possible exceptions. Do not do anything with the synchronous mode yet, that comes as a later step.
Test your solution: 
Connect to the server with your chat client. Then open the reference client app and see if you appear there as an anonymous user.
Try to connect to a wrong host (for example datakomm.wrok) and see what happens. The application should not crash, it should show an error message and go back to the menu. The current_state should be “disconnected” (unchanged).
You can also analyze it using Wireshark. Do you see the packets for the three-way-handshake?
Step 2: Implement disconnect
In a similar manner implement the disconnection function. Look for “TODO Step 2” in the code, read the hints in the comments.
Step 3: Switch to synchronous mode
It is important to do this as soon as possible after the connection establishment, before receiving any message from the server (mental exercise: think - why is that? What would happen if before switching to synchronous mode the server sent a public message from another user to your TCP client application?).
Therefore we do that right in the connect_to_server() function. 
Steps:
First, implement send_command() function. It should send a command and optional arguments to the server, according to the protocol. You will reuse this function in many later steps of this assignment.
Read the protocol documentation and find out how to switch to the synchronous mode. Implement it.
Test if it works correctly. Use wireshark to analyze traffic between your TCP client and TCP server (once you see some packets appearing, you can choose “Follow > TCP Stream” to see the traffic). Do you see a “sync” message sent from the client to the server? Do you see the “modeok” response from the server? Don’t go further until this works, otherwise the rest of the steps will not make sense (will not work, most likely).
Step 4: Wait for server to accept synchronous mode
In the previous step you asked the server to switch to the synchronous mode, but you did not check the response from the server (modeok). We do that in this step:
Implement function get_servers_response(). It should read one command (one line of text) from the server. See the “TODO Step 4” and hints.
Implement a reaction to the server’s “modeok” response - read it from the socket, check if you really got “modeok”. If you get something else (the server may respond with “cmderr command not supported”), you should print an error message.
Step 5: Login
Implement authorization (login):
Implement the necessary code, see the hints in the template code. One new thing that you will do in this step - you will need to define a new function and then refer to it in the available_actions. I.e., you need to tell the menu action configuration that when the user chooses action #3 (which is “Authorize (log in)”), your login() function must be called.
Test it:
Analyze traffic with wireshark. Do you see packets as expected?
Run the reference chat client application and connect to the same chat server. Do you see the AnonymousX user changing the username accordingly?
Step 6:  Send a public message to server
In this step, you should:
Implement sending of a public message. Again: see hints.
Test your solution – open the provided reference chat client application, connect to the server, send a message from your app and see in the reference client if your message appears in the public chat.
Step 7: List users - undocumented feature
In this step you will develop a support for an undocumented feature. From the reference client app you see that there is a possibility to find out currently active users of the chat. Use Wireshark or other tools and do some reverse engineering - find out what is the protocol to get the list of users! What does the client send to the server to poll for active users? What does the server send in response? Then go ahead and implement getting the list of users. Print them out for the user of your application.
Hint: here is a tutorial on how to use Wireshark to find out the protocol of an existing client-server conversation. 
Step 8: Send a private message
Once you see the list of users, you can also send a private message. This step will be similar to sending a public message, but you will need to ask the user to enter also the recipient name from the keyboard.
Test your solution with the reference chat application: run the app twice, log in to the public server as two different users. Try to send both public and private messages. Check if only the necessary recipients receive it.
Step 9: Print the contents of the inbox
Read the protocol - how can you check the content of your inbox? 
How many messages are stored in your inbox?
How to print out all the messages?
Send the necessary commands to the server, and print the received messages (messages from other users stored in your inbox). You can decide on some kind of user-friendly way to show the messages.
Hint: in this step the server may respond with more than one line of text!
When you are done, test your application and be proud of yourself! You have made a chat application. “Chat for en bedre verden”! :)
Optional tasks: additional features for the chat client
If you want additional exercise, you can choose to implement some extra features for the chat client.
Joke command
Ask the server a joke. This feature is not documented, but you can find it out, if you hack a bit ;) 
Print the joke for the user.
Optional tasks: implement your own chat server
This part is an optional exercise. You can try it to get a taste of programming the server side. Server is typically a bit more challenging, because it has to consider several parallel client connections and sometimes synchronize data flow between the clients, etc.
Write your own chat server. Implement the protocol described above. The server should be multi-threaded, supporting multiple parallel clients. Message forwarding should work correctly.
One challenge is to decide what happens in which thread. Hint: when you receive a message from a client, forward it to all the recipient clients on the same thread. All the client threads can listen for incoming data on the socket and sleep until they get something.
There are several ways to implement the server:
Do everything yourself for maximum challenge.
Follow the suggested steps described below. It will be easier to break down the whole task into smaller steps.
You can take a look at an existing server implementation that we provide in a GIT repository (unfortunately, in Java). The commits there are step by step implementation of the server. You can check a specific comment to see how step X was implemented.
Suggested steps
You can choose your own approach to implement the server. Here we show only steps which you can use as a guide to make the process easier. Although it seems like a lot of steps, the resulting server code is actually simpler than the chat client, because the client has a lot of complexity due to GUI-specific code.
Create a simple class or function that opens a Server socket, waits for a client to connect, prints something to the console when a client connects, and exists.
Try to connect with a chat client to your server, see if it works.
Make a while loop where you accept new client connections and call a method that handles each new connection. Put a delay of 10 sec in that processing method to simulate that the server is having conversation with the client for a while. 
Test by connecting from several clients at the same time, see that the second client will have to wait 10 sec until the first client is done.
Move the processing of a single client to a separate class (or function), call it ClientHandler. This class will be responsible for holding state for each client.
Make the server multi-threaded: one thread per client. Store the socket belonging to the client in the ClientHandler object.
Test it with several clients and make sure that a second client can connect even while processing the first one is in progress.
Make a collection where you will store all active client connections. Suggested collection structure: a dictionary with integer keys and ClientHandler objects (or function pointers) as values. It will store the ClientHandler object for each thread. Remember, that each thread represents one client connection. Therefore, by getting the ID of the current thread you will be able to get the socket and associated streams for it.
Make the server listen for incoming messages from the clients and print them out in the console: when a message x is received, print out the thread ID of the client who sent the message (use threading.get_ident()  to get thread ID) and the message itself. Use read_one_line() to read the messages: one line of data is one message.
Create a method send(message) in the class ClientHandler. It should send the message to this particular client (the socket belonging to the client).
Use the send(msg) method to echo the message back to the client. Test it in some way, for example, with Wireshark.
Generate a random ID for every new client, store it in the ClientHandler object. Make sure that the IDs are unique for all the users! Hint: you could use a global counter and generate each new ID as user1, user2, etc.
Upgrade the echo message. When client X sends you a message, reply it back to the same client, but add the clients ID in the front. For example, if client #3 sent you message “hello”, you could send back to the same client a message with text 
msg user3 hello
Modify the forwarding. Instead of echoing the message back to the same user, forward it to all other users. Hint: iterate over the collection of connections and send the message to all clients except the one belonging to this active thread.
At this point you should have a server that supports public chat for several anonymous users. Test it with the reference chat client, and pat yourself on the shoulder if it works! :)
Implement error response if you receive a command that is not supported.
Implement the help command that lists all the commands that the server supports.
Implement login. When a client wants to log in, check currently taken usernames, and either assign the username to the client and send OK back, or send an error message back.
Implement user listing. To find out the protocol (what incoming messages to look for and how to respond) use wireshark to sniff packets between the provided client and chat server.
Implement private message support. It will be very similar to public messages. The only difference: forward it only to the client who has matching username, not all the clients.
Remove a username (and associated data) from the connection list when a connection is closed.
Test the server with a chat client.
That’s it! Congratulations - you have implemented a multi-threaded TCP server which can connect people to make a better world! :)
You can now get creative and implement some of the optional commands. Then you can brag about your effort to the teachers, assistants and other students! :)
Optional tasks: extra challenges for chat server
Random joke
When the server receives the following command from a client:
	joke\n
It responds with a single command containing a random joke in the following form:
joke <joke text>\n
where <joke text> is a random joke. The text should not include any newline characters. 
Filter out spam
If one client is sending more than 10 messages per second, block messages from that client for 10 seconds. You should probably also send some kind of error message back to the client, at least the first time when you ignore the incoming message.
