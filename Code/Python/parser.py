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

        """   
        h = test()
        h.append(2)
        h.append('m')
        h.append("hi sith")
        print h.getval()
        if in map            
        """
    
    return map    

myfile = 'input.json'
data = parser(myfile)
