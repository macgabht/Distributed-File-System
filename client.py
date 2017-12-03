import socket, sys, pdb # Import socket module
import client_util


connections = {'ServerA' : 22222,
               'ServerB' : 22223,
               'Locking' : 22224,
               'Directory': 22226,
               }


RECV_BUFFER = 1024
host = socket.gethostname()
port = connections['Directory']

s = client_util.create_socket_dir((host, port))
message = client_util.dir_finder(s) #will contain info on file...
sys.stdout.write(message)

msg = message.split()
file_name = msg[1]
directory = msg[3]
server_name = msg[5]
file_server_port = msg[7] #later on create functions to tidy up this part
        
s.close() #close directory socket then create new one

#s = client_util.create_socket_dir((host, port))
#done = sys.stdin.readline()
#ack = s.recv(RECV_BUFFER)
#print ack
PORT = int(file_server_port) #should connect to relevant server 
d = client_util.create_socket_ser((host, PORT))
option = d.recv(RECV_BUFFER) #received option from server 
sys.stdout.write(option) #write this to screen. "What file do you want?"
reply = file_name
d.send(reply)

which = d.recv(RECV_BUFFER) #'read or write??'
sys.stdout.write(which)
option = sys.stdin.readline() #read or write statementcmd
d.send(option)
client_util.handle_option(option, file_name, d, PORT, host)


