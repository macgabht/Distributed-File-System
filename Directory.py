#Directory Server

import socket, sys, pdb
port = 22226
s = socket.socket()
HOST = socket.gethostname()
s.bind((HOST, port)) 
s.listen(5)
RECV_BUFFER = 1024
 

print 'Directory Server listening for file requests.....'
directory_lists = {}
directory_lists = {'File1.txt' : "directory1",
                   'File2.txt' : "directory1",
                   'File3.txt' : "directory2",
                   'File4.txt' : "directory2",
                   'File5.txt':  "directory3",
                   'File6.txt' : "directory3",
                   'File7.txt' : "directory4",
                   'File8.txt' : "directory4",
                   'File9.txt' : "directory5",
                   'File10.txt' : "directory5",
                   'File11.txt':  "directory6",
                   'File12.txt' : "directory6",
                   
                   
                   }       
dic_serv = {}
dic_serv['directory1'] = 'serverA'
dic_serv['directory2'] = 'serverA'
dic_serv['directory3'] = 'serverA'
dic_serv['directory4'] = 'serverB'
dic_serv['directory5'] = 'serverB'
dic_serv['directory6'] = 'serverB'

server_port={}
server_port['serverA'] = 22222
server_port['serverB'] = 22223
mapping={}
mapping =   {
            'File1\n': 'File1.txt',
            'File2\n': 'File2.txt',
            'File3\n': 'File3.txt',
            'File4\n': 'File4.txt',
            'File5\n': 'File5.txt',
            'File6\n': 'File6.txt',
            'File7\n': 'File7.txt',
            'File8\n': 'File8.txt',
            'File9\n': 'File9.txt',
            'File10\n': 'File10.txt',
            'File11\n': 'File11.txt',
            'File12\n': 'File12.txt',
            }


def find_value(value):
    if value in mapping:
        tmp = mapping[value]
        return tmp
        
def find_dir(number):       
    if number in directory_lists:
        temp = directory_lists[number]
        return temp
        
    
def find_serv(x):
    if x in dic_serv:
        temp = dic_serv[x]
        return temp

def find_port(num):
    if num in server_port:
        h = server_port[num]
        return h



while True:
    
     conn, address = s.accept()
     print ('Connection from: ', address)
     conn.send('Please send me the name of the file..') 
     data = conn.recv(RECV_BUFFER)
     print 'File received from user: ' + str(data)      
     file_name = find_value(data) #gives file names
     directory = find_dir(file_name)      #give the directory
     serv = find_serv(directory)     #gives the server
     serv_port = find_port(serv)     #gives the server PORT

     if file_name == 'None':
        message = 'Sorry we could not find that file'

     else:
         message = ('File_name: ' + str(file_name) + '\nDirectory: ' +str(directory)
         + '\nServer_Name: ' + str(serv) + '\nServer_Port: ' + str(serv_port) + '\n')
        
     conn.send(message)
     conn.close
     
     
     

    







                



