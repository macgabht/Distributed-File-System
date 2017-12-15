import socket, sys, os


port = 22222 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
s.bind ((HOST, port))
s.listen(5)
RECV_BUFFER = 1024

file_updates = {}
#{'File1.txt' : Version Number}
#if first time file is accessed, make zero

print ('Server A is listening.....')

#initially just stored the files in the same directory as the serverA python
#script but trying to implement file paths instead, as this could be handy for
#updating versions
#need to implement file numbers

def reply(answer, option, conn):
        if answer[0] == "Write_completed":
                msg = ('Write was successful: ' + str(answer[1]))
                conn.send(msg.encode())
        elif answer is not IOError and option == '<read>': #send the string to client to read
                conn.send(answer.encode())
                print ('String was successfully sent.')

def replication(file_name):
        print ('Sending file for replication.')
        fr = open(file_name, 'rb')
        writing = fr.read()
        fr.close()

        message = ("Replicating: " + str(file_name) + '\nEdit: ' + str(writing))

        server_port_b = 22228 
        print ('Sending rep file to serverB')
        rep_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rep_sock.connect((HOST, server_port_b))
        rep_sock.send(message.encode())
        rep_sock.close()


        #server_port_c = 22229
        #print ('Sending rep file to serverC')
        #rep_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #rep_sock.connect((HOST, server_port_c))
        #rep_sock.send(message.encode())
        #rep_sock.close()
     

def handle_msg(file_name, writing, option, file_updates):
        if '<read>' in option:
                print ('opening file to read')
                f = open(file_name, 'rb')
                ft = f.read()
                read_text = str(ft)
                return(read_text)
        elif '<write>' in option: #check if first time file written to
                if file_name not in file_updates:
                        file_upd = 0
                        file_updates[file_name] = file_upd
                else:
                        file_updates[file_name] = file_updates[file_name] + 1     
                        print (file_updates)
                        
                f = open(file_name, 'w')
                f.write(writing)
                print ('Successfully wrote to file')
                replication(file_name)
                
                return ('Write_completed', file_updates[file_name])

                #----------should give us a file number to return------------------------------#
                #------in here try and implement some sort of version checking/replication------#

def main():

        while 1:
                conn, address = s.accept()
                print ('Connection from: ', address)
                msg = conn.recv(RECV_BUFFER)
                msg = msg.decode()
                msg2 = msg.split()
        

                if 'Check_File' in msg2[1]:
                        print ('Checking File version')
                        file_name = msg2[3]
                        if not file_name in file_updates:
                                ('File yet to be edited.')
                                resp = ('0')
                                conn.send(resp.encode())
                        else:
                                file_upd = file_updates[file_name]
                                print ('Sending our file version number.')
                                conn.send(file_upd.encode())

                #-------------Replication from other file server-------------#

                elif 'Replicating' in msg2[0]:
                        r_file_name = msg2[1]
                        r_edit = msg2[3]
                        print (msg)
                        fr = open(r_file_name, 'w')
                        fr.write(r_edit)
                        fr.close()
                        print ("Replication completed on: " + str(r_file_name))

                #--------------Reading and writing as normal-------------#             
                elif msg != ' ' and 'Check_File' not in msg:
                        print (msg2)
                        file_name = msg2[1]
                        option = msg2[3]
                        msg3 = msg.split(':')
                        writing = msg3[3]
                        print ('Option selected by user: ' + str(option) + '\nFile Name: ' + str(file_name))
                        answer = handle_msg(file_name, writing, option, file_updates)
                        reply(answer, option, conn)

        conn.close()
                

if __name__ == "__main__":
        main()

                       

        
                        
                        
                      
        


