# File: reporter.py
#
# Description: Logging functions inherited by every event-generating element
# in our simulation.
# 
# Last Revised: 1 November 2015 by Sushant Sundaresh
# 					created

class Reporter:

	ID = "";

	def __init__(self,ID):        
		self.ID = ID

	def get_id (self):
		return self.ID

	def log (self, message):		
		print "Element %s reports %s\n" % (self.get_id(), message)
		return 0
