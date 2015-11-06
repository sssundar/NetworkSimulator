'''
Link & LinkBuffer Code

Operation
	LinkBuffers are just arrays. They keep track of the byte size of their
	contents, and use that to determine whether new arrivals are dropped.

	Links have a bit of telepathy. They take on initialization their
	left and right node IDs, their rate in bits/s, their propagation delay
	in seconds, and their buffer size (for each of the left/right buffers)
	in bits.

Last Revised by Sith Domrongkitchaiporn & Sushant Sundaresh on 5 Nov 2015
'''

from reporter import Reporter
from link_buffer import LinkBuffer

# The class Link extends the class Reporter
class Link(Reporter):

	left_node = ""
	right_node = ""
	bit_rate = -1 
	prop_delay = -1
	buff_bits = -1 	
	left_buff = []
	right_buff = []
	sim = ""

	# Call Node initialization code, with the Node ID (required unique)
	# Initializes itself
	def __init__(self, identity, left, right, rate, delay, size):
		Reporter.__init__(self, identity)				
		self.left_node = left
		self.right_node = right
		self.bit_rate = int(rate)
		self.prop_delay = int(delay)
		self.buff_bits = int(size)

		self.left_buff = LinkBuffer(self.buff_bits)
		self.right_buff = LinkBuffer(self.buff_bits)

	def set_event_simulator (self, sim):
		self.sim = sim
		self.left_buff.set_event_simulator(sim)
		self.right_buff.set_event_simulator(sim)

	def get_left(self):
		return self.left_node

	def get_right(self):
		return self.right_node

	def get_rate(self):
		return self.bit_rate

	def get_delay(self):
		return self.prop_delay

	def get_buff(self):
		return self.buff_bits

'''
The link cannot act like a stoplight; we'll get large fluctuations in queueing 
delay and our TCP algorithms will not stabilize.

Let's make a packet in the buffer (time_queued, packet). 

Now, when we send a packet, we just ask the system to transfer next packet.
If there's nothing in transit, we send whichever of the buffers has a head
with the smaller timestamp.

If there is something in transit, it checks.. does its origin have a packet
that could be sent and arrive before the earliest in the other end of the link

When something in transit arrives, it ...

'''

class Link extends Reporter
	private Switch_Link_Direction dir_time_out; 
	private Transmission_Callback tx_callback = null;

	private method void transfer_next_packet (Link_Queue q) {
		double current_time = this.sim.get_current_time();
		double time_left = this.time_out.get_completion_time() - current_time;		

		if q.isMyDirection(this.current_direction) {			
			if (not tx_callback == null AND not tx_callback.is_active()) {				
				if q.can_dequeue() {					
					Packet potential_tx = q.head();
					double channel_loading_delay = 
						((double) potential_tx.bit_length()) / this.capacity;

					if (channel_loading_delay + propagation_delay < time_left) {

						this.tx_callback = 
							new Transmission_Callback(
								this,
								q,
								current_time+channel_loading_delay);
						this.sim.request_event(this.tx_callback);			
						
						this.sim.request_event(
							Handle_Packet_Arrival(
								q.dequeue(), 
								current_time + channel_loading_delay + 
									propagation_delay
									)
								);
					}
				}	
			}
		}
	}


	-- how a Node attempts to send a packet through this link
	public method void send (Packet p, Node source) {
		if ( source.get_id() = left_node.get_id() ) {
			-- Transfer Requested Left -> Right
			if left_queue.can_enqueue(p) {
				left_queue.enqueue(p);
				transfer_next_packet(left_queue);
			} else {
				log("packet dropped at " . this.sim.get_current_time());
			}			
		} else {
			-- Transfer Requested Right -> Left
			if right_queue.can_enqueue(p) {
				right_queue.enqueue(p);
				transfer_next_packet(right_queue);
			} else {
				log("packet dropped at " . this.sim.get_current_time());
			}			
		}		
	}
