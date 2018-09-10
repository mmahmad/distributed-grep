import unittest
from client import Client

class TestLogQuerier(unittest.TestCase):

	def test_rare_patterns(self):
		result = Client('grep -n "^Machine number"', is_test = True).query()
		num_lines = result.count('\n')

		self.assertEqual(num_lines, 1)
		for line in result[:-1].split('\n'):
			self.assertIn('Machine number', line)

	def test_somewhat_frequent_patterns(self):
		result = Client('grep -n "^Somewhat frequent"', is_test = True).query()
		num_lines = result.count('\n')

		self.assertEqual(num_lines, 10)
		for line in result[:-1].split('\n'):
			self.assertIn('Somewhat frequent', line)

	def test_frequent_patterns(self):
		result = Client('grep -n "^Very frequent"', is_test = True).query()
		num_lines = result.count('\n')

		self.assertEqual(num_lines, 50)
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
		self.assertIn('machine.1', result)
		self.assertNotIn('machine.2', result)
		self.assertNotIn('machine.3', result)
		self.assertIn('1-11111', result)

	def test_occur_in_some_logs(self):
		pass

	def test_occur_in_all_logs(self):
		pass

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestLogQuerier)
	unittest.TextTestRunner(verbosity=2).run(suite)