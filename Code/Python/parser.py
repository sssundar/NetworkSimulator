# Parser Code
# Sith Domrongkitchaiporn

import json
from host import Host
from link import Link
from router import Router
from flow import Flow

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
			f = Flow(line["id"], line["source"], line["dest"], line["size"],line["start"])
			map[line["id"]] = f 

			# Set flow for the hosts
			map[line["source"]].set_flow(line["id"])
			map[line["dest"]].set_flow(line["id"])    

	return map    

myfile = 'input.json'
data = parser(myfile)