# Working Unit Test Benches for Network Simulator 
# Last Revised: 14 November 2015 by Sushant Sundaresh & Sith Domrongkitchaiporn
'''
IMPORTANT: Please turn off logging  (MEASUREMENT_ENABLE = False) in constants.py
before running these testbenches.
'''

# Unit Testing Framework
import unittest

# Test Modules
import reporter, node, host, link, router
import flow, event_simulator, event, events
import link, link_buffer, packet
import constants
from static_flow_test_node import *
import visualize

class testMeasurementAnalysis (unittest.TestCase):
	'''
		Tests visualize.py time-averaging function
	'''

	def test_time_averaging (self):
		self.assertTrue(visualize.test_windowed_time_average())

class TestStaticDataSinkFlow (unittest.TestCase):
	'''
		### Might break for dynamic TCP ### 
		if this is implemented on receiver side as well

		Create Flow Data Sink
		Create Static_Data_Sink_Test_Node	
		Tell Flow its number or expected packets
		Create Event Simulator 

		For now:
		Ask flow to receive a packet, check that Ack has same packet ID
		Ask flow to receive the same packet again, should get same result.
	'''
	
	sim = "" # event simulator
	f = "" # flow, data source, static
	n = "" # test node

	def setUp (self):				
		self.f = flow.Data_Sink("f1sink","h2","h1",\
			3*constants.DATA_PACKET_BITWIDTH, 1.0)
		self.n = Static_Data_Sink_Test_Node ("h2","f1sink")
		self.sim = event_simulator.Event_Simulator({"f1sink":self.f,"h2":self.n})
		self.f.set_flow_size(2)

	def test_basic_ack (self):
		packets = [	packet.Packet("f1source","h1","h2","",0,0), \
					packet.Packet("f1source","h1","h2","",1,0)]
		self.n.receive(packets[0])
		self.assertEqual(self.n.head_of_tx_buff(),0)
		self.n.receive(packets[1])
		self.assertEqual(self.n.head_of_tx_buff(),1)
		# Two packets received, two packets acknowledged
		with self.assertRaises(ValueError):
			self.n.head_of_tx_buff()
		# Repeated packets just get repeated acks
		self.n.receive(packets[1])
		self.assertEqual(self.n.head_of_tx_buff(),1)

class TestStaticDataSourceFlow (unittest.TestCase):
	'''
		### Will break for dynamic TCP ###	
			Assumes Flow (Data Source) Window Size
			hard-coded to 2

		Create Flow Data Source 
		Create Static_Data_Source_Test_Node	
		Create Event Simulator 
		Start Flow -> pokes tcp -> sends two packets to Node
		Check that these were sent to Node

		Fake Acks through Node to Flow
		Check that this updates Node Tx_Buffer (more sends from Flow)

		Check what Timeout Does
	'''
	sim = "" # event simulator
	f = "" # flow, data source, static
	n = "" # test node

	def setUp (self):				
		self.f = flow.Data_Source("f1","h1","h2",\
			3*constants.DATA_PACKET_BITWIDTH, 1.0) 
		self.n = Static_Data_Source_Test_Node ("h1","f1")
		self.sim = event_simulator.Event_Simulator({"f1":self.f,"h1":self.n})

	def test_static_flow_source (self):
		# The first static flow source implementation
		# just has packets/acks have the same id. 
		# There is no chance of 'duplicate acks' to indicate loss
		
		self.f.start() # do this manually so don't have to run simulator

		self.assertEqual(self.n.head_of_tx_buff(),0)
		
		packet1 = self.n.tx_buff[0]
		
		self.assertEqual(self.n.head_of_tx_buff(),1)		
		with self.assertRaises(ValueError):
			self.n.head_of_tx_buff()
		
		self.n.receive(packet.Packet("","h2","h1",\
				constants.DATA_PACKET_ACKNOWLEDGEMENT_TYPE,\
				0,constants.DATA_ACK_BITWIDTH))
		
		self.assertEqual(self.n.head_of_tx_buff(),2)
		with self.assertRaises(ValueError):
			self.n.head_of_tx_buff()		
		
		self.f.time_out(packet1) 
		
		# check that next packet has id 1
		self.assertEqual(self.n.head_of_tx_buff(),1)


class TestLinkTransmissionEvents(unittest.TestCase):	
	sim = "" # simulator
	link = "" # link
	lNode = "" # left node 
	rNode = "" # right node
	lPs = [] # left packets 
	rPs = [] # right packets

	# Create Event Simulator
	# Create Link & Nodes (not Hosts, so don't need working Flow) on either side
	# Create three packets from either side, to the other, and send them.	
	def setUp (self):
		self.lNode = node.Node("h1")
		self.rNode = node.Node("h2")
		# don't need flow, as no packet timeouts created to callback to flow
		# and node receive is a dummy function		
		for i in 1, 2, 3:
			self.lPs.append(packet.Packet("","h1","h2","data",i,1000)) # 1000kbit
			self.rPs.append(packet.Packet("","h2","h1","data",i,1000))
		
		self.link = link.Link("l1", "h1", "h2", 1000.0, 10.0, 3000.0) 
					# 1000kbit/ms, 10 ms prop delay, 3000kbit buffers

		self.sim = event_simulator.Event_Simulator({"l1":self.link, \
													"h1":self.lNode, \
													"h2":self.rNode})
	# Order the packet sends 2L-2R-L-R
	# Run Sim Forward
	# Watch for transmission events in EventSimulator, with proper timestamp
	# Watch for propagation events in EventSimulator, with proper timestamp
	# Make sure these are sequential, with only one Tx event at a time in
	# the queue, and two propagations in each direction chained, and one isolated.
	# Note this tests most events we're trying to deal with.
	def test_packet_callbacks_and_timing (self):
		self.link.send(self.rPs.pop(0),"h2")  	# right going packets
											# are favored in time tie breaks
		self.link.send(self.rPs.pop(0),"h2") 
		self.link.send(self.rPs.pop(0),"h2") 
		self.link.send(self.lPs.pop(0),"h1") 
										# all have timestamp 0.0
										# so link should switch directions
										# between each packet

		# Confirm Handle_Packet_Transmission events show up in EventSim
		# with proper timestamps
		self.assertTrue(self.sim.get_current_time() == 0)
		self.sim.run_next_event()
		self.assertTrue(self.sim.get_current_time() == 1) 	
															# right packet1 load
															# into channel at 
															# 1ms going h2->h1
		self.assertTrue(self.link.transmission_direction == constants.RTL)
		
		self.sim.run_next_event()
		self.assertTrue(self.sim.get_current_time() == 11)  
															# propagation done
															# direction switched
															# next packet loaded
															# LTR
		self.assertTrue(self.link.transmission_direction == constants.LTR)										
													# next event is a load (12)
													# then a propagation (22)
													# then 
													# the next event should be
													# both remaining h2 packets
													# loaded, as left buffer 
													# is empty 
		self.sim.run_next_event()
		self.assertTrue(self.sim.get_current_time() == 12)
		self.sim.run_next_event()
		self.assertTrue(self.sim.get_current_time() == 22)
		self.assertTrue(self.link.transmission_direction == constants.RTL)	
		self.sim.run_next_event()
		self.sim.run_next_event() 		# two loads
		self.assertTrue(self.sim.get_current_time() == 24)
		self.assertTrue(self.link.transmission_direction == constants.RTL)										
		self.sim.run_next_event() 		# two propagations
		self.sim.run_next_event() 		
		self.assertTrue(self.link.transmission_direction == constants.RTL)										
		self.assertTrue(self.sim.get_current_time() == 34)
		
class TestLinkBuffer(unittest.TestCase):
	# test variables
	l = "" # a link buffer
	p = "" # a packet exactly half the size of the buffer
	s = "" # event simulator

	def setUp (self):
		c = 100 # buffer capacity in bits
		self.s = event_simulator.Event_Simulator({})
		self.l = link_buffer.LinkBuffer(c)
		self.l.set_event_simulator(self.s)
		self.p = packet.Packet("","","","","",c/2)

	def test_enqueue_dequeue (self):
		self.assertTrue(self.l.can_enqueue(self.p))
		self.l.enqueue(self.p)
		self.assertTrue(self.l.can_enqueue(self.p))
		self.l.enqueue(self.p)
		self.assertFalse(self.l.can_enqueue(self.p))
		self.l.enqueue(self.p) # dropped
		self.l.enqueue(self.p) # dropped

		self.assertTrue(self.l.can_dequeue())
		self.assertTrue( isinstance(self.l.dequeue(),packet.Packet) )
		self.assertTrue(self.l.can_dequeue())
		self.assertTrue( isinstance(self.l.dequeue(),packet.Packet) )
		
		self.assertFalse(self.l.can_dequeue())
		with self.assertRaises(ValueError):
			self.l.dequeue()

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
			"h2":host.Host("h2",["l1"]),\
			"f1":flow.Data_Source("f1", "h1", "h2", 20, 1)})
		
		self.assertEqual(e.get_current_time(), 0.0)
		self.assertFalse(e.are_flows_done())
		
		self.assertEqual(e.get_element("h1").get_id(), "h1")
		self.assertEqual(e.get_element("h2").get_id(), "h2")
		self.assertEqual(e.get_element("f1").get_id(), "f1")

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
		self.assertEqual(self.l.get_rate(),float(self.rate))
	def test_get_delay(self):	
		self.assertEqual(self.l.get_delay(),float(self.delay))
	def test_get_buff(self):	
		self.assertEqual(self.l.get_buff(),float(self.buff) * 8.0) # bytes to bits

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
		self.assertEqual(f.get_size(), int(size) * 8.0 * 1000.0) # MByte -> KBit
		self.assertEqual(f.get_start(), int(start) * 1000) # s to ms

# Run Specific Tests
if __name__ == "__main__":
	reporter_suite = unittest.TestLoader().loadTestsFromTestCase(TestReporter)
	node_suite = unittest.TestLoader().loadTestsFromTestCase(TestNode)
	host_suite = unittest.TestLoader().loadTestsFromTestCase(TestHost)
	link_suite = unittest.TestLoader().loadTestsFromTestCase(TestLink)
	router_suite = unittest.TestLoader().loadTestsFromTestCase(TestRouter)
	flow_suite = unittest.TestLoader().loadTestsFromTestCase(TestFlow)
	sim_suite = unittest.TestLoader().loadTestsFromTestCase(TestEventSimulator)
	linkbuffer_suite = unittest.TestLoader().loadTestsFromTestCase(TestLinkBuffer)
	link_tx_suite = unittest.TestLoader().loadTestsFromTestCase(TestLinkTransmissionEvents)
	static_flow_data_source_suite = \
		unittest.TestLoader().loadTestsFromTestCase(TestStaticDataSourceFlow)
	static_flow_data_sink_suite = \
		unittest.TestLoader().loadTestsFromTestCase(TestStaticDataSinkFlow)
	visualize_suite = \
		unittest.TestLoader().loadTestsFromTestCase(testMeasurementAnalysis)


	test_suites = [reporter_suite, node_suite, host_suite, link_suite,\
					router_suite, flow_suite, sim_suite, linkbuffer_suite,\
					link_tx_suite,static_flow_data_source_suite,\
					static_flow_data_sink_suite, visualize_suite]

	for suite in test_suites:
		unittest.TextTestRunner(verbosity=2).run(suite)		
		print "\n\n\n"