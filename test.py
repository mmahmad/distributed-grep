import unittest
from client import Client

NUM_MACHINES = 1

class TestLogQuerier(unittest.TestCase):

	def test_rare_patterns(self):
		result = Client('grep -n "^Machine number"', is_test = True).query()
		num_lines = result.count('\n')

		self.assertEqual(num_lines, NUM_MACHINES)
		for line in result[:-1].split('\n'):
			self.assertIn('Machine number', line)

	def test_somewhat_frequent_patterns(self):
		result = Client('grep -n "^Somewhat frequent"', is_test = True).query()
		num_lines = result.count('\n')

		self.assertEqual(num_lines, 10 * NUM_MACHINES)
		for line in result[:-1].split('\n'):
			self.assertIn('Somewhat frequent', line)

	def test_frequent_patterns(self):
		result = Client('grep -n "^Very frequent"', is_test = True).query()
		num_lines = result.count('\n')

		self.assertEqual(num_lines, 50 * NUM_MACHINES)
		for line in result[:-1].split('\n'):
			self.assertIn('Very frequent', line)

	def test_does_not_occur(self):
		result = Client('grep -n "This string does not occur', is_test = True).query()
		num_lines = result.count('\n')

		self.assertEqual(num_lines, 0)

	def test_occur_in_one_log(self):
		result = Client('grep -n -G "1-1*"', is_test = True).query()
		num_lines = result.count('\n')

		self.assertEqual(num_lines, 1)
		self.assertIn('1-11111', result)
		self.assertIn('machine.1', result)

		for machine_number in range(2, NUM_MACHINES + 1):
			self.assertNotIn('machine.{}'.format(machine_number), result)
		
	def test_occur_in_some_logs(self):
		result = Client('grep -n "^Only in odd"', is_test = True).query()
		num_lines = result.count('\n')

		if NUM_MACHINES % 2 == 0:
			self.assertEqual(num_lines, 10 * (NUM_MACHINES/2))
		else:
			self.assertEqual(num_lines, 10 * (NUM_MACHINES/2 + 1))

		#Check that no lines from even numbered machines have been matched, and lines from 
		#all odd numbered machines are present
		for machine_number in range(1, NUM_MACHINES + 1):
			if machine_number % 2 == 0:
				self.assertNotIn('machine.{}'.format(machine_number), result)
			else:
				self.assertIn('machine.{}'.format(machine_number), result)

	def test_occur_in_all_logs(self):
		result = Client('grep -n "^Machine number"', is_test = True).query()
		num_lines = result.count('\n')

		self.assertEqual(num_lines, NUM_MACHINES)

		for i in range(1, NUM_MACHINES):
			self.assertIn('machine.{}'.format(i), result)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestLogQuerier)
	unittest.TextTestRunner(verbosity=2).run(suite)