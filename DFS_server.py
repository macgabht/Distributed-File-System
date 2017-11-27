import socket

port = 22222 
s = socket.socket()
HOST = socket.gethostname()
s.bind ((HOST, port))
s.listen(5)
RECV_BUFFER = 4096

print 'Server listening.....'

while True:

        conn, address = s.accept()
        print 'Connection from', address
        data = conn.recv(RECV_BUFFER)
        print ('Server received,' repr(data))

        filename = 'mytext.txt'
        f = open(filename, 'rb')
        l = f.read(RECV_BUFFER)
        while (1):
            conn.send(l)
            print ('Sent ', repr(l))
            l = f.read(1024)

        f.close()

        print ('Done sending')
        conn.send('Thanks for connecting')
        conn.close()

        


