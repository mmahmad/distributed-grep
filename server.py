import socket # socket module
import subprocess # to execute system calls

# import thread module 
from thread import *
import threading

def get_process_hostname():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
    s.close()

# thread fuction 
def threaded(conn): 
     
    # data received from client 
    command = conn.recv(1024) 
    if not command: 
        print 'No command'
        conn.close()
        return

    command = command.strip() # to remove empty whitespaces, added due to large (1024 bytes) buffer
    print 'received command: ' + command
    try:
        retData = subprocess.check_output(command, shell=True)
    except:
        # In case no match found
        print "CalledProcessError: No match found"
        conn.close()
        return

    retData = retData[:-1] # to remove the final \n
    # '1:import socket\n2:import os\n# not needed 3:import subprocess\n'
    print "retData: " + retData
    conn.sendall(retData) # send all will break down text in small packets and then send all the packets

    conn.close() # close the connection

def Main():

    #create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind the socket to host and custom port
    PROCESS_INIT_PORT, PROCESS_HOSTNAME = 45000, get_process_hostname()
    serversocket.bind((PROCESS_HOSTNAME, PROCESS_INIT_PORT))
    #become a server socket
    serversocket.listen(5)

    print "Waiting for client to connect..."

    while (1):
        conn, addr = serversocket.accept()
        print 'Connected with:' + addr[0] + ':' + str(addr[1])

        # Start a new thread and return its identifier 
        start_new_thread(threaded, (conn,)) 

    # no need to close socket, otherwise will need to start up server again...
    # serversocket.close()

if __name__ == '__main__': 
    Main()