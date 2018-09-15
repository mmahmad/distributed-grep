import json
from server import get_process_hostname
import random, socket

def generate_logs():
	with open('config.json') as config:
		config_data = json.load(config)

	current_ip = get_process_hostname()
	host = socket.gethostbyaddr(current_ip)[0]
	server_id = [server['id'] for server in config_data['servers'] if server['host'] == host][0]

	patterns = []


	#1. Only occuring in one log file
	patterns.append(server_id + '-' + server_id * 5 + '\n')

	#2. Occuring in some log files - only in log files with odd server_ids
	if int(server_id) % 2 == 1:
		for i in range(10):
			patterns.append('Only in odd numbered files - ' + str(i) + '\n')

	#3. Occuring in all log files

	#Rare pattern - once per log file
	patterns.append('Machine number - ' + str(server_id) + '\n')

	#Somewhat frequent patterns
	for i in range(10):
		patterns.append('Somewhat frequent pattern - ' + str(i) + '\n')

	#Very frequent patterns
	for i in range(50):
		patterns.append('Very frequent pattern - ' + str(i) + '\n')


	#Add some unknown lines to log files
	for i in range(30):
		patterns.append(str(random.getrandbits(50)) + '\n')

	random.shuffle(patterns)
	with open('machine.{}.test.log'.format(server_id), 'w') as file:
		file.writelines(patterns)

if __name__ == '__main__':
	generate_logs()
