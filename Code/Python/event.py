''' 
event.py is the parent class for all events 
It simply stores its completion time and has an accessor to this time.
It's event action is to do nothing.

Sushant Sundaresh
'''

class Event ():

	completion_time = 0.0

	def __init__(self):
		pass
	
	def event_action(self, sim):
		pass

	def set_completion_time(self, time):
		self.completion_time = time
		return self

	def get_completion_time(self):
		return self.completion_time