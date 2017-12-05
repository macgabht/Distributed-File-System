import socket, sys, pdb, Lock_ut # Import socket module
from Lock_ut import FileLock


RECV_BUFFER = 1024

def create_socket_ser(address):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address) #set up connection, communicate with Directory
        return s

def create_socket_dir(address):
        d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        d.connect(address) #set up connection, communicate with Directory
        return d
        

def dir_finder(file_name, opt, s):
    option = s.recv(RECV_BUFFER) #"what file would you like to search for?"
    option = option.decode()
    print (option) #write this to screen
    print (file_name) #print out file_name, automatically send
    data = (str(file_name) + ' ' + str(opt))
    s.send(data.encode())
    answer = s.recv(RECV_BUFFER) #this is where we receive from directory service, this won't change
    answer = answer.decode()
    return answer #should return fn, server name, server port

def process_write(file_name, opt, host, port):
        
        s = create_socket_dir((host, port)) #create connection to directory, we have file_name
        response = dir_finder(file_name, opt, s) #get answer from directory
        #**********
        msg = response.split()
        file_name = msg[1]
        server_name = msg[3]
        file_server_port = msg[5] #have info on file, need to pass name to locking
        print (msg)

        ####skip locking for moment, connect to file server
        PORT = int(file_server_port)
        d = create_socket_ser((host, PORT)) #connection from....
        print ('Create your text edit...signal the end with <DONE>.\n')
        text_edit = ''
        while True:
                
                text_edit = sys.stdin.readline()
                if '<DONE>' in text_edit:
                    break
                else:
                     send_edit += text_edit
        print ('n')

        message = ('FILE_NAME: ' + str(file_name) + '\nOPTION: ' + str(opt) + '\nEDIT: ' + str(send_edit)) 
        s.send(message.encode())
        

        

        
                        
        
        
        
        
        
        
        
        
        
def handle_option(msg, file_name, s, port, host):
    file_n = str(file_name)
    if 'read' in msg:
        with open(file_n, 'rb') as f: 
            print('file opened')
            while True:
                data = s.recv(RECV_BUFFER)
                print('receiving data to read...')
                print(data)
                if not data:
                    break
                
        f.close()
        print('Successfully read the file\n')
        s.close()
        
    elif 'write' in msg:
        with open(file_n, 'wb') as f: #file written to directory DFS
            print ('file opened')
            while True:
                data = s.recv(RECV_BUFFER)
                print('receiving data to write...')
                print(data) #print data to screen
                if not data:
                    break
        f.close()
        print('Successfully read file, ready to edit')
        s.close() #close socket and reopen it again
        print('connection closed')

        n = create_socket_ser((host, port))
        serv = n.recv(RECV_BUFFER) #which file do you want?
        print (serv)
        print (file_n)
        n.send(file_n) #send our file_name back
        option = n.recv(RECV_BUFFER)
        print (option)
        opt = sys.stdin.readline()
        n.send(opt)
        print ('Please enter your edit to the file')
        edit = sys.stdin.readline()
        n.send(edit)
        print ('edit sent')
        n.close()
      
                    
    else:
        error = ('That was not one of the options given')
        sys.stdout.write(error)
        print('Failure to get files.\n')
        s.close()
        print('connection closed due to error')



        
        
