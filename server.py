import socket # socket module
import subprocess # to execute system calls

# import thread module 
# from _thread import *
# import threading 

PROCESS_INIT_PORT = 45000
PROCESS_HOSTNAME = '10.193.204.192'

#create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
# serversocket.bind((socket.gethostname(), PROCESS_INIT_PORT))
serversocket.bind((PROCESS_HOSTNAME, PROCESS_INIT_PORT))
#become a server socket
serversocket.listen(5)

print "Waiting for client to connect..."

# while (1):
# 	#accept connections from outside (server waits until there is a connection to accept)
#     (connection, address) = serversocket.accept()
#     #now do something with the clientsocket
#     #in this case, we'll pretend this is a threaded server
#     # ct = client_thread(clientsocket)
#     # ct.run()

#     print 'Connected with ' + address[0] + ':' + str(address[1])
# 	connection.send('Connection to server successful. Please type you command and press enter.')
# 	while (1):
# 		data = conn.recv(1024)
# 		connection.send('Executing command \'' + data + '\'')
# 		print data


while (1):
    conn, addr = serversocket.accept()
    print 'Connected with:' + addr[0] + ':' + str(addr[1])
    # conn.send('connected to server! Type command, then press enter: ')
    command = conn.recv(1024)
    command = command.strip()
    print 'received command: ' + command
    # retData = call('ls')
    retData = subprocess.check_output(command, shell=True)
    # '1:import socket\n2:import os\n# not needed 3:import subprocess\n'
    print "retData: " + retData
    conn.sendall(retData) # send all will break down text in small packets and then send all the packets
    conn.close() # close the connection


# class mysocket:
#     '''demonstration class only
#       - coded for clarity, not efficiency
#     '''

#     def __init__(self, sock=None):
#         if sock is None:
#             self.sock = socket.socket(
#                 socket.AF_INET, socket.SOCK_STREAM)
#         else:
#             self.sock = sock

#     def connect(self, host, port):
#         self.sock.connect((host, port))

#     def mysend(self, msg):
#         totalsent = 0
#         while totalsent < MSGLEN:
#             sent = self.sock.send(msg[totalsent:])
#             if sent == 0:
#                 raise RuntimeError("socket connection broken")
#             totalsent = totalsent + sent

#     def myreceive(self):
#         chunks = []
#         bytes_recd = 0
#         while bytes_recd < MSGLEN:
#             chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
#             if chunk == '':
#                 raise RuntimeError("socket connection broken")
#             chunks.append(chunk)
#             bytes_recd = bytes_recd + len(chunk)
#         return ''.join(chunks)


# x = mysocket()