#Directory Server

import socket, sys, pdb, os
import csv


port = 22226
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
s.bind((HOST, port)) 
s.listen(5)
RECV_BUFFER = 1024

print ('Directory Server listening for file requests.....')

def find_file(file_name):

    with open('mapping.csv', 'rt') as fn: 
        readin = csv.DictReader(fn, delimiter = ',') #splits the cells by commas
        header = readin.fieldnames
        for row in readin:
            input_file = row['User_input']
            if input_file == file_name:
                real_file = row['File_name']
                print (real_file)
                server_name = row['Server_Name']
                print (server_name)
                server_port = row['server_port']
                message = ('File_Name: ' + str(real_file) + '\nServer_Name: ' + str(server_name) + '\nServer_Port: ' + str(server_port))
                return message

def main():
    
    while True:
    
        conn, address = s.accept()
        print ('Connection from: ', address)
        msg = ('What file would you like to search?')
        conn.send(msg.encode()) 
        data = conn.recv(RECV_BUFFER)
        data = data.decode()
        print ('File received from user: ' + str(data))      
        fn = data.split()[0]
        option = data.split()[1]
        answer = find_file(fn)
        
        if answer is not None:
            answer = str(answer)
            print ('answer: \n' + answer)
            print("\n")

        else:
            answer = ('NO SUCH FILE IN THIS DIRECTORY')
            print ('answer: \n' + answer)
            print ("\n")

        conn.send(answer.encode())
        ##maybe try the locking on another server.."

    
        with FileLock(data):
            #work with the file as it is now locked

            print("Lock acquired.")
            conn.send(answer.encode()
        

        conn.close
     
if __name__ == "__main__":
        main()
     

    







                



