# Parser Code
# Sith Domrongkitchaiporn

import json
from host import *
from link import *
from router import *
from flow import *

"""
Parser Function

Input:      .json file  (Example = input.json)
return:     hash table(nodes)

Nodes can be flow, link, router or host. Check input.json for the format.

"""

def parser (myfile):
	with open(myfile) as file:    
		data = json.load(file)

	map = {}    # Create Hash Table   

	for line in data:
		line["type"]

		if line["type"] == "host":
			print "H"
			h = Host(line["id"], line["links"])
			map[line["id"]] = h            

		elif line["type"] == "link":
			print "L"
			l = Link(line["id"], line["left"], line["right"], line["rate"], line["delay"], line["buffer"])
			map[line["id"]] = l

		elif line["type"] == "router":
			print "R"
			r = Router(line["id"], line["links"])
			map[line["id"]] = r

		elif line["type"] == "flow":
			print "F"
			ds = Data_Source(line["id"], line["source"], line["dest"], line["size"],line["start"])
			dd = Data_Sink(line["id"], line["dest"], line["source"], line["size"],line["start"])		# Dest and Src is swapped for sink

			keys = line["id"] + "_src"
			keyd = line["id"] + "_dest"

			map[keys] = ds
			map[keyd] = dd

			# Set flow for the hosts
			map[line["source"]].set_flow(keys)
			map[line["dest"]].set_flow(keyd)    

	return map    

myfile = 'input.json'
data = parser(myfile)