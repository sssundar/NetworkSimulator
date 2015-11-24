import sys, os
import json
import matplotlib.pyplot as plt

t = []
v = []
flag = True
with open("results/l1_bufferoccupancy_left-to-right.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t.append(line[0])
			v.append(line[1])

ax1 = plt.subplot(211)
plt.plot(t,v)

t = []
v = []
flag = True
with open("results/l1_bufferoccupancy_right-to-left.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t.append(line[0])
			v.append(line[1])

plt.subplot(212, sharex=ax1)
plt.plot(t,v)

plt.show()