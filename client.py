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
			sock.settimeout(1.0)   
			sock.connect((self.host, int(self.port)))
		except socket.error as e: #If connection to remote machine fails
			print 'Could not connect to ' + str(self.host)
			return

		try:
			sock.sendall(self.command)

			while True:
				part = sock.recv(10240000)
				if part:
					self.result += part
				else:
					if self.result:
						self.queue.put({self.logfile_name: self.result})
					break

		except socket.error as e:
			return

class Client(object):

	def __init__(self, command, is_test):
		self.command = command
		self.is_test = is_test
		with open('config.json') as config:
			config_data = json.load(config)
		self.servers = config_data['servers']
		self.port = config_data['port']
		self.queue = Queue.Queue()

	def query(self):
		thread_list = []
		output = ''

		for server in self.servers:
			host = server['host']

			if self.is_test:
				thread = QueryThread(self.command, host, self.port, server['test_logfile_name'], self.queue)
			else:
				thread = QueryThread(self.command, host, self.port, server['logfile_name'], self.queue)
				
			thread.start()
			thread_list.append(thread)


		for thread in thread_list:	
			thread.join()

		lines_matched = []

		while not self.queue.empty():
			item = self.queue.get()
			file_name, result = item.keys()[0], item.values()[0]
			output += (result + '\n')

			if not self.is_test:
				print 'File name: ' + (file_name)
				print result
				lines_matched.append('File name: ' + file_name + ', Number of lines: ' + str(result.count('\n') + 1))

		print ''
		if not self.is_test:
			for line in lines_matched:
				print line
			print 'Total lines matched:%s' % (output.count('\n'))
		
		return output

def main():
	while True:
		command = raw_input('\nEnter grep command...\n')
		obj = Client(command, is_test = False)
		obj.query()

if __name__ == '__main__':
	main()