import socket, sys, os

Directory1 = []
Directory1 = ['File1.txt', 'File2.txt, File3.txt']

port = 22222 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST = 'localhost'
s.bind ((HOST, port))
s.listen(5)
RECV_BUFFER = 1024

print 'Server A is listening.....'

#initially just stored the files in the same directory as the serverA python
#script but trying to implement file paths instead, as this could be handy for
#updating versions if we get that far


def reply(answer, option, conn):
        if answer[0] == "Write_completed":
                msg = ('Write was successful.')
                conn.send(msg.encode())
        elif answer[0] is not IOError and option == 'read':
                conn.send(answer[0].encode())
                

def handle_msg(file_name, edit, option):
        if 'read' in option:
                f = open(file_name, 'rb')
                file_text = f.read()
                return(file_text)
        elif 'write' in option:
                f = open(file_name, 'wb')
                f.write(edit)
                return ('Write_completed')
#####in here try and implement some sort of version checking/replication######
                
        

def main():

        while 1:
                conn, address = s.accept()
                print ('Connection from: ', address)
                msg = conn.recv(RECV_BUFFER)
                msg = msg.decode()
                msg2 = msg.split()
                file_name = msg[1]
                option = msg[3]
                edit = msg[5]

                print ('File requested by user: ' + str(data)+'\nOption: ' + str(option))
                answer = handle_msg(file_name, edit, option)
                reply(answer, option, conn)

        conn.close()
                

if __name__ == "__main__"
        main()

                       

        
                        
                        
                      
        


