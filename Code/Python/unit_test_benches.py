# Working Unit Test Benches for Network Simulator 
# Last Revised: 1 November 2015 by Sushant Sundaresh

# Unit Testing Framework
import unittest

# Test Modules
import reporter, node, host

class TestReporter(unittest.TestCase):
  
	# Set ID of reporter
	def test_get_id(self):
		ID = "H1"
		r = reporter.Reporter(ID)
		r.log("Hello World!")
		self.assertEqual(r.get_id(), ID)

class TestNode(unittest.TestCase):

	# Set ID of node through super initialiation
	def test_init(self):
		ID = "H2"
		n = node.Node(ID)
		n.log("Hello World!")
		self.assertEqual(n.get_id(), ID)

	# Should not break, as receive is a dummy function
	def test_receive(self):
		ID = "H2"
		n = node.Node(ID)
		n.receive(0)

class TestHost(unittest.TestCase):

	# Set ID of host through super initialiation
	def test_init(self):
		ID = "H1"
		Links = ["L1"]
		h = host.Host(ID,Links)
		h.log("Hello World!")
		self.assertEqual(h.get_id(), ID)
		self.assertEqual(h.get_element_type(), constants.HOST_ELEMENT)
		with self.assertRaises(ValueError):
			h2 = host.Host(ID,["L1","L2"])					
	
	def test_sendreceive(self):		
		# Should break, as flows not yet implemented in Python
		ID = "H1"
		Links = ["L1"]
		h = host.Host(ID,Links)		
		h.receive("nothing")
		h.send("nothing")

# Run Specific Tests
if __name__ == "__main__":
	reporter_suite = unittest.TestLoader().loadTestsFromTestCase(TestReporter)
	node_suite = unittest.TestLoader().loadTestsFromTestCase(TestNode)
	host_suite = unittest.TestLoader().loadTestsFromTestCase(TestHost)
	
	test_suites = [reporter_suite, node_suite, host_suite]
	for suite in test_suites:
		unittest.TextTestRunner(verbosity=2).run(suite)		