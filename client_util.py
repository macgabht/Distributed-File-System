import socket, sys, pdb # Import socket module

RECV_BUFFER = 1024

def create_socket_ser(address):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect(address) #set up connection, communicate with Directory
        return s

def create_socket_dir(address):
        d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        d.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        d.connect(address) #set up connection, communicate with Directory
        return d
        

def dir_finder(s):
    option = s.recv(RECV_BUFFER) #received option from server 
    print (option) #write this to screen
    file_name = sys.stdin.readline() #write the file name in 
    s.send(file_name)
    answer = s.recv(RECV_BUFFER) #this is where we receive from directory service, this won't change
    return answer

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



        
        
