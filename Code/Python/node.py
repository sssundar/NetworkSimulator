# File: node.py
#
# Description: a host or a router, both of which can report state to the logs
# 
# Last Revised: 1 November 2015 by Sushant Sundaresh
# 					created

from reporter import Reporter

# The class Node extends the class Reporter
class Node(Reporter):

	# Call Reporter initialization code, with the Node ID (required unique)
	def __init__(self, ID):
		Reporter.__init__(self, ID)				

	# This function must be overridden
	def receive (self, packet):
		pass 