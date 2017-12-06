import socket, sys, pdb 

connections = {'ServerA' : 22222,
               'ServerB' : 22223,
               'Locking' : 22224,
               'Directory': 22226,
               }

RECV_BUFFER = 1024

def create_socket_ser(address):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address) #set up connection, communicate with Directory
        return s

def create_socket_dir(address):
        d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        d.connect(address) #set up connection, communicate with Directory
        return d
        

def dir_finder(file_name, opt, s, JOIN_ID):
        option = s.recv(RECV_BUFFER) #"what file would you like to search for?"
        option = option.decode()
        print (option) #write this to screen
        print (file_name) #print out file_name, automatically send
        data = (str(file_name) + ' ' + str(opt) + ' ' + str(JOIN_ID))
        s.send(data.encode())
        answer = s.recv(RECV_BUFFER) #this is where we receive from directory service, this won't change
        answer = answer.decode()
        return answer #should return fn, server name, server port

def talk_to_locking(file_name, l, JOIN_ID, u_l): #unlock-lock
        data = (str(u_l) + '-' + str(file_name)+'-'+str(JOIN_ID))
        print (data)
        l.send(data.encode())
        reply = l.recv(RECV_BUFFER)
        reply = reply.decode()
        return reply
                

def write_to_fs(file_name, opt, s):
        print ('Create your text edit...signal the end with <DONE>.\n')
        send_edit = ''
        while True:
                text_edit = sys.stdin.readline()
                if '<DONE>' in text_edit:
                    break
                else:
                     send_edit += text_edit
                     
        print ('--------')
        message = ('FILE_NAME: ' + str(file_name) + '\nOPTION: ' + str(opt) + '\nEDIT: ' + str(send_edit)) 
        s.send(message.encode())
        reply = s.recv(RECV_BUFFER)
        reply = reply.decode()
        return reply


def read_to_fs(file_name, opt, r):
        print ('Sending read request to File Server')
        message = ("File_name: " +str(file_name) + '\nOption: ' + str(opt) + '\nEdit: ' + '-')
        print (message)
        r.send(message.encode())
        rec = r.recv(RECV_BUFFER)
        rec = rec.decode()
        return rec
        

def process_write(file_name, opt, host, port, JOIN_ID):
        s = create_socket_dir((host, port)) #create connection to directory, we have file_name
        response = dir_finder(file_name, opt, s, JOIN_ID) #get answer from directory
        msg = response.split()
        file_name = msg[1]
        server_name = msg[3]
        file_server_port = msg[5] #have info on file, need to pass name to locking
        print (msg)
        s.close()
        ############################################################
        #########LOCKING########
        PORT = connections['Locking']
        l = create_socket_ser((host, PORT))
        u_l = 'lock'
        print ('Your join_id is: ' + str(JOIN_ID))
        print ("To gain a lock, format the string as such: lock-file_name-JOIN_ID")
        lock_ans = talk_to_locking(file_name, l, JOIN_ID, u_l)
        print (lock_ans)
        l.close()
        ##############################################################
        #               file server                                  #
        PORT = int(file_server_port)
        print ('Now connecting to file server..')
        d = create_socket_ser((host, PORT))
        response = write_to_fs(file_name, opt, s)
        if response == 'Write was successful.':
               print (response)
        
        
                
def process_read(file_name, opt, host, port, JOIN_ID):
        s = create_socket_dir((host, port)) #create connection to directory, we have file_name
        response = dir_finder(file_name, opt, s, JOIN_ID) #get answer from directory
        msg = response.split()
        file_name = msg[1]
        server_name = msg[3]
        file_server_port = msg[5] #have info on file, need to pass name to locking
        print (msg)
        s.close()
        print (opt)
        print ('Now connecting to file server...')
        PORT = int(file_server_port)
        r = create_socket_ser((host, PORT)) #connection from....
        read_file = read_to_fs(file_name, opt, r)
        r.close()
        if read_file != "File could_not_be_found_here\n":
               print (read_file)
               
        
        

        
        
