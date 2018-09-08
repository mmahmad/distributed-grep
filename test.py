import unittest
from client import Client

class TestLogQuerier(unittest.TestCase):
	 def test_two_files(self):
	 	command = "grep -n 'self.host = host'"
	 	obj = Client(command)

	 	expected_output = 'Filename:client.py, Line 11:\t\tself.host = host '
	 	self.assertEqual(expected_output, obj.query())

if __name__ == '__main__':
    unittest.main()