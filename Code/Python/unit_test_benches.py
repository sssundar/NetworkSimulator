# Working Unit Test Benches for Network Simulator 
# Last Revised: 1 November 2015 by Sushant Sundaresh

# Unit Testing Framework
import unittest

# Test Modules
import reporter, node, host, link, router, flow

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

class TestLink(unittest.TestCase):

	# Set ID of link through super initialiation
	def test_init(self):
		ID = "L1"
		left = "H1"
		right = "H2"
		rate = "10"
		delay = "10"
		buff = "64"
		l = link.Link(ID,left,right,rate,delay,buff)
		self.assertEqual(l.get_id(), ID)
		self.assertEqual(l.get_left(),left)
		self.assertEqual(l.get_right(),right)
		self.assertEqual(l.get_rate(),int(rate))
		self.assertEqual(l.get_delay(),int(delay))
		self.assertEqual(l.get_buff(),int(buff))

class TestRouter(unittest.TestCase):

	# Set ID of link through super initialiation
	def test_init(self):
		ID = "R1"
		links = ["H1","H2","H3"]
		r = router.Router(ID,links)
		self.assertEqual(r.get_id(), ID)
		self.assertEqual(r.get_link(),links)

class TestFlow(unittest.TestCase):

	# Set ID of link through super initialiation
	def test_init(self):
		ID = "F1"
		source = "H1"
		dest = "H2"
		size = "20"
		start =  "1"

		f = flow.Flow(ID,source,dest,size,start)
		self.assertEqual(f.get_id(), ID)
		self.assertEqual(f.get_source(), source)
		self.assertEqual(f.get_dest(), dest)
		self.assertEqual(f.get_size(), int(size))
		self.assertEqual(f.get_start(), int(start))

# Run Specific Tests
if __name__ == "__main__":
	reporter_suite = unittest.TestLoader().loadTestsFromTestCase(TestReporter)
	node_suite = unittest.TestLoader().loadTestsFromTestCase(TestNode)
	host_suite = unittest.TestLoader().loadTestsFromTestCase(TestHost)
	link_suite = unittest.TestLoader().loadTestsFromTestCase(TestLink)
	router_suite = unittest.TestLoader().loadTestsFromTestCase(TestRouter)
	flow_suite = unittest.TestLoader().loadTestsFromTestCase(TestFlow)

	test_suites = [reporter_suite, node_suite, host_suite, link_suite, router_suite, flow_suite]
	for suite in test_suites:
		unittest.TextTestRunner(verbosity=2).run(suite)		