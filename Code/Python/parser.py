"""
Parser File
@ Sith Domrongkitchaiporn

"""

#%%
import json
from test import Test as test

def parser (myfile):
    with open(myfile) as file:    
        data = json.load(file)
    
    map = {}    
    
    for line in data:
        print line["type"]
                
        if line["type"] == "host":
            print "H"
            if line["id"] not in map:
                h = host()
                map[line["id"]] = h            
            map[line["id"]].addlink(line["links"])
        elif line["type"] == "link":
            print "L"
            if line["id"] not in map:
                l = link()
                map[line["id"]] = l            
            map[line["id"]].addnode(line["left"],line["right"])
            map[line["id"]].addconst(line["rate"],line["delay"],line["buffer"])
        elif line["type"] == "router":
            print "R"
        elif line["type"] == "flow":
            print "F"
            if line["id"] not in map:
                f = flow()
                map[line["id"]] = f            
            map[line["id"]].addflow(line["source"],line["dest"])
            map[line["id"]].addconst(line["size"],line["start"])
            
            """   
           h = test()
            h.append(2)
            h.append('m')
            h.append("hi sith")
            print h.getval()
            if in map            
        """
    
    return data    

myfile = 'input.json'
data = parser(myfile)
