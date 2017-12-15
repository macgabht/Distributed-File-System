#Locking Server
import socket, sys, pdb
import os
import time
import errno

port = 22224
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
s.bind((HOST, port)) 
s.listen(5)
RECV_BUFFER = 1024

print ('Locking Server listening for lock requests.....')

class FileLockException(Exception):
    pass

class FileLock:

    def __init__(self, file_name):
        #---------Prepare the locker. Specify the file to lock---------#
        #---------Timeout is made to zero here --------------#
        self.is_locked = False
        self.lockfile = os.path.join(os.getcwd(), "%s.lock" % file_name)
        self.file_name = file_name
        self.timeout = 0
        self.delay = 0.5
        self.lock_status = {} #dict to store file_name and join_id

    def parse_message(self, option, fn, JOIN_ID):
                
        if 'lock' in option:
            if not self.is_locked:
                fn = self.file_name
                reply = self.acquire(fn, JOIN_ID)
                return reply

        elif 'unlock' in option:
             if self.file_name in self.lock_status: #player returns having used the lock
                    if self.lock_status[file_name] == JOIN_ID:
                        reply = self.release()
                        del self.lock_status[file_name]
                        return reply
             else:
                    print ('Unable to unlock file, user misprint.')             


    def acquire(self, fn, JOIN_ID):
        #Acquire the lock, if possible. If the lock is in use, it check again
        #every `wait` seconds. It does this until it either gets the lock or
        #exceeds `timeout` number of seconds, in which case it throws 
        #an exception.
        
        start_time = time.time()
        while True:
            try:
                print (self.lockfile)
                self.fd = os.open(self.lockfile, os.O_CREAT|os.O_EXCL|os.O_RDWR)
                break;
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise 
                if (time.time() - start_time) >= self.timeout:
                    raise FileLockException("Timeout occured.")
                time.sleep(self.delay)
        self.is_locked = True
        self.lock_status[fn] = JOIN_ID #obtained lock, add to dict
        return ('LA')


    def release(self):
        
        #----------Get rid of the lock by deleting the lockfile.------------# 
 
        if self.is_locked:
            os.close(self.fd)
            os.unlink(self.lockfile)
            self.is_locked = False

        return ('LR')



def main():


    while True:
        conn, address = s.accept()
        print('Connection from: ', address)
        msg = conn.recv(RECV_BUFFER)
        msg = msg.decode() #should contain three values
        print (msg)
        message = str(msg)
        x = message.split()
        file_name = x[1] #client sends 'lock'/'unlock'-File_name-JOIN_ID...
        option = x[3]
        JOIN_ID = x[5]
        fl = FileLock(file_name)
        status = fl.parse_message(option, file_name, JOIN_ID)
        if 'LA' in status:
            print ('Lock Achieved')
            x = ('Lock_Achieved')
        elif 'LR' in status:
            print ('Lock released')
            x = ('Lock_Released')

        conn.send(x.encode())
                        
        conn.close()

if __name__ == "__main__":
    main()

            
        

