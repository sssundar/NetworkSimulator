# Parser Code
# Sith Domrongkitchaiporn

import json
from host import host
from link import link
from router import router
from flow import flow

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
		print line["type"]

	if line["type"] == "host":
		print "H"
		h = host(line["id"], line["links"])
		map[line["id"]] = h            
            
	elif line["type"] == "link":
		print "L"
		l = link(line["id"], line["left"], line["right"], line["rate"], line["delay"], line["buffer"])
		map[line["id"]] = l
            
	elif line["type"] == "router":
		print "R"
		r = router(line["id"], line["links"])
		map[line["id"]] = r

	elif line["type"] == "flow":
            print "F"
            f = flow(line["id"], line["source"], line["dest"], line["size"],line["start"])
            map[line["id"]] = f 
            
            # Set flow for the hosts
            map[line["source"]].set_flow(line["id"])
            map[line["dest"]].set_flow(line["id"])    

	return map    

myfile = 'input.json'
data = parser(myfile)