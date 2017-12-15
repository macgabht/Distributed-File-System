import socket, sys, pdb, os.path 

connections = {'ServerA' : 22222,
               'ServerB' : 22223,
               'Locking' : 22224,
               'Directory': 22226,
               }

cache_path = "C:\\Users\\tiarnan\\Documents\\DFS\\Cache\\"
RECV_BUFFER = 1024
file_updates = {} #use this to check if files are up-to-date 

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
        data = ('File_name: ' + str(file_name) + '\nOption: ' + str(u_l) + '\nJoin_Id: ' + str(JOIN_ID))
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
        message = ('FILE_NAME: ' + str(file_name) + '\nOPTION: ' + str(opt) + '\nEDIT: ' + (send_edit)) 
        s.send(message.encode())
        reply = s.recv(RECV_BUFFER)
        reply = reply.decode() #reply will contain two values, "Write  Completed", file_no.
        msg3 = reply.split()
        answer = (msg3[0], msg3[1], send_edit)
        return answer

def check_file_updates(file_name, file_updates, r_s):
        msg = ('Option: ' + 'Check_File' +'\nFile_name: ' + str(file_name) + '\nEdit: ' + str('-'))
        print (msg)
        r_s.send(msg.encode())
        file_ver = r_s.recv(RECV_BUFFER)
        file_ver = file_ver.decode()
        file_ver = int(file_ver)
        if file_ver == 0:
                print ('File yet to be edited.')
                file_updates[file_name] = file_ver
                resp = '0'
                return resp
        
        elif file_updates[file_name] == file_ver:  #MATCHING, USE CACHE
                print ('File version matches ours, use cache to access.')
                resp = '1'
                return resp
        else:
                print('File has been edited since our last access, cache file no longer relevant.')
                print ('Request new copy.')
                resp = ('2', file_ver)
                return resp
        
        
def read_to_fs(file_name, opt, r_s):
        print ('Sending read request to File Server, with file number.')
        message = ("File_name: " +str(file_name) + '\nOption: ' + str(opt) + '\nEdit: ' + '-')
        print (message)
        r_s.send(message.encode())
        rec = r_s.recv(RECV_BUFFER)
        rec = rec.decode()
        return rec
        

def process_write(file_name, opt, host, port, JOIN_ID):
        s = create_socket_dir((host, port)) #create connection to directory, we have file_name
        response = dir_finder(file_name, opt, s, JOIN_ID) #get answer from directory
        msg = response.split()
        file_name = msg[1]
        server_name = msg[3]
        file_server_port = msg[5] #have info on file from directory, need to pass name to locking
        print (msg)
        s.close()
        
        #-------LOCKING------------#
        PORT = connections['Locking']
        l = create_socket_ser((host, PORT))
        u_l = 'lock'
        print ('Your join_id is: ' + str(JOIN_ID))
        lock_ans = talk_to_locking(file_name, l, JOIN_ID, u_l)
        print (lock_ans)
        if 'Lock_Achieved' in lock_ans:
                 l.close()
                 print ('Redirecting to file server now.')
        
        if not lock_ans:
                print('Error occurred during the locking stage.\n')
                l.close()

        # ----------file server-------------------#
        #-------we don't check file versions when writing as it will have to be updated in server dict anyway-----#
        
        PORT = int(file_server_port)
        print ('Now connecting to file server..')
        d = create_socket_ser((host, PORT))
        response = write_to_fs(file_name, opt, d)
        if msg[0] == 'Write was successful.': 
               print (msg[0])
               print ('Please update your version number of the file')
               file_upd = int(msg[1])
               print (msg[1]) #gives us a file version number
               edit = msg[2]
               file_updates[file_name] = file_upd #updated our version of the file in our dict
               use_cache(file_name, edit, opt, file_updates)

        #--------back to locking to unlock the file----------------#
        print('User is finished with this file. Reopening locking connection\n')
        PORT = connections['Locking']
        l = create_socket_ser((host, PORT))
        u_l = 'unlock'      
        lock_ans = talk_to_locking(file_name, l, JOIN_ID, u_l)
        if 'Lock_released' in lock_ans:
                print ('Succesfully unlocked the file.')
        
def process_read(file_name, opt, host, port, JOIN_ID):
        s = create_socket_dir((host, port)) #create connection to directory, we have file_name
        response = dir_finder(file_name, opt, s, JOIN_ID) #get answer from directory
        msg = response.split()
        file_name = msg[1]
        server_name = msg[3]
        file_server_port = msg[5] #have info on file
        print (msg)
        s.close()
        print (opt)
        print ('Now connecting to file server...')
        print ('Checking File number first.')
        PORT = int(file_server_port)
        r_s = create_socket_ser((host, PORT)) #connection from....
        response = check_file_updates(file_name, file_updates, r_s)#connect to FS to check version
        r_s.close()
        #------When reading a file, we don't look to achieve a lock on it-------------#
        #------close socket and reopen to file server------#
        
        read_s = create_socket_ser((host, PORT))

        if response == '0': #carry on as normal
                print ('response = 0')
                read_file = read_to_fs(file_name, opt, read_s)
                opt = 'write'
                use_cache(file_name, read_file, opt, file_updates)
                read_s.close()
                print (read_file)
                if read_file != "File could_not_be_found_here\n":
                         print(read_file)
        elif response == '1':
                         print ('Accessing file from cache')
                         use_cache(file_name, '-', opt, file_updates)
                         read_s.close()
        elif response[0] == '2': #carry on as normal, update the file version, after reading overwrite the file in the cache
                        file_ver = response[2]
                        read_file = read_to_fs(file_name, opt, read_s)
                        file_updates[file_name] = file_ver #update the version of the file in our dict
                        opt = 'write' #after reading, write it to our cache 
                        use_cache(file_name, read_file, opt, file_updates)
                        read_s.close()


#------Caching - files are written to same directory the client is in ----------------#

def use_cache(file_name, send_edit, opt, file_updates):
        print ('Using cache.')
        cache_f = os.path.join(cache_path, file_name) #join path, write file to cache after r/w

        if opt == '<read>':
                with open(cache_f, 'r') as fc:
                       print(fc.read)
        else:
                with open(cache_f, 'w') as fc:
                        fc.write(send_edit)

                
        
