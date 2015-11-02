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
    
    for line in data:
        print line["type"]
        if line["type"] == "host":
            h = test()
            h.append(2)
            h.append('m')
            h.append("hi sith")
            print h.getval()
        elif line["type"] == "link":
            print "L"
        elif line["type"] == "router":
            print "R"
        elif line["type"] == "flow":
            print "F"
    
    return data    

myfile = 'input.json'
data = parser(myfile)
