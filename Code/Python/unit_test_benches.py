# Working Unit Test Benches for Network Simulator 
# Last Revised: 1 November 2015 by Sushant Sundaresh

# Unit Testing Framework
import unittest

# Test Modules
import reporter, node, host, link, flow, event_simulator, event

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

class TestEventSimulator(unittest.TestCase):
	def test_init_and_basic_simulation (self):
		e = event_simulator.Event_Simulator({"h1":host.Host("h1",["l1"]),\
			"h2":host.Host("h2",["l1"])})
		self.assertEqual(e.get_current_time(), 0.0)
		self.assertFalse(e.are_flows_done())
		self.assertEqual(e.get_element("h1").get_id(), "h1")
		self.assertEqual(e.get_element("h2").get_id(), "h2")
		e.request_event(event.Event().set_completion_time(1.0))
		e.request_event(event.Event().set_completion_time(2.0))
		e.request_event(event.Event().set_completion_time(0.5))
		e.request_event(event.Event().set_completion_time(1.5))
		e.request_event(event.Event().set_completion_time(0.2))
		''' Now event heap should be ordered 0.2, 0.5, 1, 1.5, 2 '''
		e.run_next_event()
		self.assertEqual(e.get_current_time(), 0.2)
		e.run_next_event()
		self.assertEqual(e.get_current_time(), 0.5)
		e.run_next_event()
		self.assertEqual(e.get_current_time(), 1.0)				
		e.run_next_event()
		self.assertEqual(e.get_current_time(), 1.5)
		e.run_next_event()
		self.assertEqual(e.get_current_time(), 2.0)

class TestHost(unittest.TestCase):

	# Set ID of host through super initialiation
	def test_init(self):
		ID = "H1"
		Links = ["L1"]
		h = host.Host(ID,Links)
		h.log("Hello World!")
		self.assertEqual(h.get_id(), ID)		
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
		rate = 10
		delay = 10
		buff = 64
		l = link.Link(ID,left,right,rate,delay,buff)
		self.assertEqual(l.get_id(), ID)
		self.assertEqual(l.get_left(),left)
		self.assertEqual(l.get_right(),right)
		self.assertEqual(l.get_rate(),rate)
	
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
	sim_suite = unittest.TestLoader().loadTestsFromTestCase(TestEventSimulator)
	
	
	test_suites = [reporter_suite, node_suite, host_suite, sim_suite]
	for suite in test_suites:
		unittest.TextTestRunner(verbosity=2).run(suite)		