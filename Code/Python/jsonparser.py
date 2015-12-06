# Parser Code
# Sith Domrongkitchaiporn

import json
from host import *
from link import *
from router import *
from flow import *
from tcp_flow import *
from tcp_reno_working import *
from tcp_vegas_working import *
from tcp_fast_working import *
from constants import *

"""
Parser Class

Input:      .json file  (Example = input.json)
return:     hash table(nodes)

Nodes can be flow, link, router or host. Check input.json for the format.

"""

class JSONParser ():

	myfile = ""

	def __init__(self,JSONFile):
		self.myfile = JSONFile

	def parser(self, tcp):
		
		with open(self.myfile) as file:    
			data = json.load(file)

		input_map = {}    # Create Hash Table   

		for line in data:
			line["type"]

			if line["type"] == "host":
				# print "H"
				h = Host(line["id"], line["links"])
				input_map[line["id"]] = h            

			elif line["type"] == "link":
				# print "L"
				l = Link(line["id"], line["left"], line["right"], line["rate"], line["delay"], line["buffer"])
				input_map[line["id"]] = l

			elif line["type"] == "router":
				# print "R"
				r = Router(line["id"], line["links"])
				input_map[line["id"]] = r

			elif line["type"] == "flow":
				# print "F"
				keys = line["id"] + "_src"
				keyd = line["id"] + "_dest"
				
				# if TCP_RENO_ENABLE is True:										
				# 	ds = Data_Source_TCP_RENO(keys, line["source"], line["dest"], line["size"],line["start"])				
				# 	dd = Data_Sink_TCP_RENO(keyd, line["dest"], line["source"], line["size"],line["start"])	# Dest and Src is swapped for sink
				# elif TCP_STATIC_ENABLE is True:					
				# 	ds = Data_Source(keys, line["source"], line["dest"], line["size"],line["start"])				
				# 	dd = Data_Sink(keyd, line["dest"], line["source"], line["size"],line["start"])	# Dest and Src is swapped for sink
				if tcp == TCP_RENO:
					ds = Working_Data_Source_TCP_RENO(keys, line["source"], line["dest"], line["size"],line["start"])				
					dd = Working_Data_Sink_TCP_RENO(keyd, line["dest"], line["source"], line["size"],line["start"])	# Dest and Src is swapped for sink
				elif tcp == TCP_VEGAS:
					ds = Working_Data_Source_TCP_VEGAS(keys, line["source"], line["dest"], line["size"],line["start"])				
					dd = Working_Data_Sink_TCP_RENO(keyd, line["dest"], line["source"], line["size"],line["start"])	# Dest and Src is swapped for sink									
				elif tcp == TCP_FAST:
					ds = Working_Data_Source_TCP_FAST(keys, line["source"], line["dest"], line["size"],line["start"])				
					dd = Working_Data_Sink_TCP_RENO(keyd, line["dest"], line["source"], line["size"],line["start"])	# Dest and Src is swapped for sink													
				else:
					raise ValueError("Invalid TCP selection: %s\n"%tcp)
					
				dd.set_flow_size(ds.get_flow_size()) # in packets

				input_map[keys] = ds
				input_map[keyd] = dd

				# Set flow for the hosts
				input_map[line["source"]].set_flow(keys)
				input_map[line["dest"]].set_flow(keyd)    

		return input_map    