# Working Unit Test Benches for Network Simulator 
# Last Revised: 1 November 2015 by Sushant Sundaresh

# Unit Testing Framework
import unittest

# Test Modules
import reporter, node, host, link, router, flow, event_simulator, event

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
	ID = ""
	left = ""
	right = ""
	rate = ""
	delay = ""
	buff = ""
	l = ""

	def setUp(self):
		self.ID = "L1"
		self.left = "H1"
		self.right = "H2"
		self.rate = "10"
		self.delay = "10"
		self.buff = "64"
		self.l = link.Link(self.ID,self.left,self.right,self.rate,self.delay,self.buff)

	# Set ID of link through super initialiation
	def test_get_id(self):	
		self.assertEqual(self.l.get_id(), self.ID)
	def test_get_left(self):	
		self.assertEqual(self.l.get_left(),self.left)
	def test_get_right(self):		
		self.assertEqual(self.l.get_right(),self.right)
	def test_get_rate(self):	
		self.assertEqual(self.l.get_rate(),int(self.rate))
	def test_get_delay(self):	
		self.assertEqual(self.l.get_delay(),int(self.delay))
	def test_get_buff(self):	
		self.assertEqual(self.l.get_buff(),int(self.buff))

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
	sim_suite = unittest.TestLoader().loadTestsFromTestCase(TestEventSimulator)

	test_suites = [reporter_suite, node_suite, host_suite, link_suite, router_suite, flow_suite, sim_suite]

	for suite in test_suites:
		unittest.TextTestRunner(verbosity=2).run(suite)		