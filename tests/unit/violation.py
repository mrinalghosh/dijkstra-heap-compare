''' Violation Heap Unit Test.'''

import unittest
from heaps import Violation


class ViolationHeapTest(unittest.TestCase):
	''' Unit Test Class for Violation Heap Implementation '''
	
	def setUp(self):
		# Do some setup of the heap.
		self.v_heap = ViolationHeap()

	def test_decrease_key(self):
		# Verify against a mock heap.
		pass