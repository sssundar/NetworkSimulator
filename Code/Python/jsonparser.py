# Parser Code
# Sith Domrongkitchaiporn

import json
from host import *
from link import *
from router import *
from flow import *

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

	def parser(self):
		
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
			
				ds = Data_Source(keys, line["source"], line["dest"], line["size"],line["start"])
				# Dest and Src is swapped for sink
				dd = Data_Sink(keyd, line["dest"], line["source"], line["size"],line["start"])	
				dd.set_flow_size(ds.get_flow_size()) # in packets

				input_map[keys] = ds
				input_map[keyd] = dd

				# Set flow for the hosts
				input_map[line["source"]].set_flow(keys)
				input_map[line["dest"]].set_flow(keyd)    

		return input_map    