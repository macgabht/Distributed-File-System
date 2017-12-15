# Distributed-File-System
Internet Applications

Tiarnan Mac Gabhann 
Student Number: 13325213

This is written in Python 3.6.3,

1. Compile the Directory Server - python directory.py (the map.csv file will be required to be in the same folder as this in order to accessed)
2. Start the Locking Server - python Locking.py
3. Start the File server(s) - python servera.py (files written to are saved as text files in the same folder as the server.py)
                            - python serverb.py
4. Start the Client - compile client.py (requires the client libraries client_util.py to be in the same folder)
 
 
Method
1. Client is prompted to either <write>/<read> to a file in the format - <write> File1
  
2. Directory server is connected to immmediately, returning information on the file. 

3. The client recieves the information on the File and is connected to the Locking server which returns a lock once it has been achieved.
4. The client is then connected to the File Server which either requests an edit if being written to, or sends the read file as a string to the client.

5. When writing a new file into its database, the file server will send a replication messsage to other servers with the updated string. 
6. After writing to a new file, the client will write the file to its cache.
7. The cache is also accessed if the client receives confirmation from the server that its current copy of a file is up to date and that  it wishes to only read it.
