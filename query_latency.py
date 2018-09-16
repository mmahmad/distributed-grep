from matplotlib import pyplot as plt
from client import Client
import time, numpy

def generate_latency_plot():
	
	y_mean, y_std = [], []
	patterns = ['ab', '99', '10', 'a']
	x = [i for i in range(len(patterns))]

	for pattern in patterns:
		y = []
		for i in range(5):
			start_time = time.time()
			grep_command = 'grep -n ' + '\"' + pattern + '\"'
			result = Client(grep_command, is_test = False).query()
			end_time = time.time()

			y.append(end_time - start_time)

		y_mean.append(numpy.mean(y))
		y_std.append(numpy.std(y))


	plt.errorbar(x, y_mean, yerr = y_std, fmt='o', barsabove = True)
	plt.xticks(x, patterns)
	plt.xlabel('Grepped Pattern')
	plt.ylabel('Query Latency (seconds)')
	plt.xlim(-1,4)
	plt.grid(True)
	plt.title('Mean query latency for different patterns with standard deviation error bars')
	plt.show()

if __name__ == '__main__':
	generate_latency_plot()