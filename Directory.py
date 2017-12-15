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

    with open('map.csv', 'rt') as csvfile: 
        reader = csv.DictReader(csvfile, delimiter = ',') #splits the cells by commas
        titles = reader.fieldnames
        for row in reader:
            #print (row['user_input'])
            input_file = row['user_input']
            if input_file == file_name:
                real_file = row['file_name']
                print (real_file)
                server_name = row['server_name']
                print (server_name)
                server_port = row['server_port']
                message = ('File_Name: ' + str(real_file) + '\nServer_Name: ' + str(server_name) + '\nServer_Port: ' + str(server_port))
                return message
            else:
                return None 

def main():
    
    while True:
    
        conn, address = s.accept()
        print ('Connection from: ', address)
        msg = ('What file would you like to search for and for what purpose?')
        conn.send(msg.encode()) 
        data = conn.recv(RECV_BUFFER)
        data = data.decode()  
        fn = data.split()[0]
        option = data.split()[1]
        JOIN_ID = data.split()[2]
        print ('File_name: ' + str(fn) + '\nOption: ' + str(option) + '\nJOIN_ID: ' + str(JOIN_ID))
        answer = find_file(fn)
        
        if answer is not None:
            answer = str(answer)
            print ('Mapping Info retrieved: \n' + answer)
            print("\n")

        else:
            answer = ('NO_SUCH_FILE')
            print ('ERROR: \n' + answer)
            print ("\n")

        conn.send(answer.encode())

        conn.close
     
if __name__ == "__main__":
        main()
     

    







                



