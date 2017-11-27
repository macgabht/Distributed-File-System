import socket, sys

port = 22222 
s = socket.socket()
HOST = socket.gethostname()
s.bind ((HOST, port))
s.listen(5)
RECV_BUFFER = 1024

print 'Server listening.....'

while True:
        
        conn, address = s.accept()
        print ('Connection from: ', address)
        conn.send('Would you like to read or write to a file? ')      
        data = conn.recv(RECV_BUFFER) #await response
        print 'Server received from user: ' + str(data)
        #data will be either 'read' or 'write'
        filename = 'test.txt'
        f = open(filename, 'rb')
        l = 1
        while (l):
        
                l = f.read(RECV_BUFFER)
                while (l):
                    conn.send(l)
                    print ('Sent ' + str(l))
                    l = f.read(RECV_BUFFER)
                        
        f.close()
        print ('Done sending files to read\n')
        conn.send('Thanks for connecting, bye')
        conn.close()

        
                        
                        
                      
        


