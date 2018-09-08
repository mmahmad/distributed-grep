import threading
import json
import socket
import Queue

class QueryThread(threading.Thread):

	def __init__(self, command, host, port, logfile_name, queue):
		super(QueryThread, self).__init__()
		self.command = command + ' ' + logfile_name
		self.host = host
		self.port = port
		self.queue = queue
		self.result = ''
		self.logfile_name = logfile_name

	def run(self):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.host, int(self.port)))
		except socket.error as e: #If connection to remote machine fails
			print 'Could not connect'
			return

		try:
			sock.sendall(self.command)

			while True:
				part = sock.recv(1024)
				if part:
					self.result += part
				else:
					self.queue.put({self.logfile_name: self.result})
					break

		except socket.error as e:
			return

class Client(object):

	def __init__(self, command):
		self.command = command
		with open('config.json') as config:
			config_data = json.load(config)
		self.servers = config_data['servers']
		self.port = config_data['port']
		self.queue = Queue.Queue()

	def query(self):
		thread_list = []

		for server in self.servers:
			host, ip = server['host'], server['ip']
			thread = QueryThread(self.command, ip, self.port, server['logfile_name'], self.queue)
			thread.start()
			thread_list.append(thread)

		for thread in thread_list:
			thread.join()

		while not self.queue.empty():
			item = self.queue.get()
			file_name, result = item.keys()[0], item.values()[0]

			for line in result.split('\n'):
				print 'Filename:%s, Line %s ' % (file_name, line)

def main():
	while True:
		command = raw_input('Enter grep command...\n')
		obj = Client(command)
		obj.query()

if __name__ == '__main__':
	main()