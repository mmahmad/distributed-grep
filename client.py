import threading
import json
import socket

class QueryThread(threading.Thread):

	def __init__(self, command, host, port):
		self.command = command
		self.host = host
		self.port = port

	def run(self):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.host, self.port))
			sock.sendall(self.command)
			
		except socket.error as e:
			pass


class Client(object):

	def __init__(self, command):
		self.command = command
		with open('config.json') as config:
			config_data = json.load(config)
		self.servers = config_data['servers']
		self.port = config_data['port']

	def query(self):
		thread_list = []

		for server in self.servers:
			host, ip = server['host'], server['ip']
			thread = QueryThread(self.command, self.ip, self.port)
			thread.start()
			thread_list.append(thread)

		for thread in thread_list:
			thread.join()

def main():
	Client('test')

if __name__ == '__main__':
	main()