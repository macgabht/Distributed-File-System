import client_util
import socket, sys 
from time import gmtime, strftime
from datetime import datetime

connections = {'ServerA' : 22222,
               'ServerB' : 22223,
               'Locking' : 22224,
               'Directory': 22226,
               }

RECV_BUFFER = 1024
host = 'localhost'

def main():
    
    JOIN_ID = strftime("%Y%m%d%H%M%S", gmtime())

    while True:

        print ('Enter write/read file_name..')
        usr_input = sys.stdin.readline()

        if "write" in usr_input:
            opt = usr_input.split()[0]
            file_name = usr_input.split()[1]
            port = connections['Directory']
            client_util.process_write(file_name, opt, host, port, JOIN_ID)

        elif "read" in usr_input:
            opt = usr_input.split()[0]
            file_name = usr_input.split()[1]
            port = connections['Directory']
            client_util.process_read(file_name, opt, host, port, JOIN_ID)
            

 
if __name__ == "__main__":
    main()
    

