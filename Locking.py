#Locking Server
#semaphores, timer, fencing tokens needed?

import socket, sys, pdb, Lock_ut
from Lock_ut import FileLock
port = 22224
s = socket.socket()
HOST = socket.gethostname()
s.bind((HOST, port)) 
s.listen(5)
RECV_BUFFER = 1024

print 'Locking Server listening for file requests.....'

while True:
    conn, address = s.accept()
    print ('Connection from: ', address)
    conn.send('Please send me the name of the file you wish to lock..') 
    data = conn.recv(RECV_BUFFER) #wait for reply 
    print 'File received from user: ' + str(data)      


with FileLock(data):
    #in here we do the bits needed
    #work with the file as it is now locked
    message = 'Contact the file server...'
    conn.send(message)
    print data
    print("Lock acquired.")
