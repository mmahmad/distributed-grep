import unittest
from client import Client

class TestLogQuerier(unittest.TestCase):
	def test_rare_patterns(self):
		pass

	def test_somewhat_frequent_patterns(self):
		pass

	def test_frequent_patterns(self):
		pass

	def test_does_not_occur(self):
		pass

	def test_occur_in_one_log(self):
		pass

	def test_occur_in_some_logs(self):
		pass

	def test_occur_in_all_logs(self):
		pass

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestLogQuerier)
	unittest.TextTestRunner(verbosity=2).run(suite)