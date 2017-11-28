import socket, sys, pdb # Import socket module

connections = {'ServerA' : 22222,
               'ServerB' : 22223,
               'Locking' : 22224,
               'Directory': 22226,
               }

s = socket.socket()             # Create a socket object
host = socket.gethostname()# Get local machine name
port = 22226    #This port will initially be connected to directory service
RECV_BUFFER = 1024
s.connect((host, port)) #set up connection, communicate with Directory
option = s.recv(RECV_BUFFER) #received option from server 
sys.stdout.write(option) #write this to screen
msg = sys.stdin.readline()
s.send(msg)
message = s.recv(RECV_BUFFER) #this is where we receive from directory service, this won't change
sys.stdout.write(message) #here we print the message from the Directory server

msg = message.split()
file_name = msg[1]
directory = msg[3]
server_name = msg[5]
File_server_port = msg[7] #later on create functions to tidy up this part

s.close() #close directory socket then create new one

t = socket.socket()
PORT = connections['Locking'] #connecting to locking
t.connect((host, PORT))
option = t.recv(RECV_BUFFER) #received option from server 
sys.stdout.write(option) #write this to screen
reply = file_name
t.send(reply)






