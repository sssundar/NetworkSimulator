import sys, os
import json
import matplotlib.pyplot as plt

t1 = []
l1ltr = []
flag = True
with open("results/l1_bufferoccupancy_left-to-right.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t1.append(line[0])
			l1ltr.append(line[1])

t2 = []
l1rtl = []
flag = True
with open("results/l1_bufferoccupancy_right-to-left.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t2.append(line[0])
			l1rtl.append(line[1])

t3 = []
l0ltr = []
flag = True
with open("results/l0_bufferoccupancy_left-to-right.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t3.append(line[0])
			l0ltr.append(line[1])

t4 = []
l0rtl = []
flag = True
with open("results/l0_bufferoccupancy_right-to-left.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t4.append(line[0])
			l0rtl.append(line[1])


t5 = []
l2ltr = []
flag = True
with open("results/l2_bufferoccupancy_left-to-right.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t5.append(line[0])
			l2ltr.append(line[1])

t6 = []
l2rtl = []
flag = True
with open("results/l2_bufferoccupancy_right-to-left.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t6.append(line[0])
			l2rtl.append(line[1])

ax1 = plt.subplot(211)
ax1.plot(t4,l0rtl,'b.', t2, l1rtl, 'ro', t6, l2rtl, 'k-')
ax2 = plt.subplot(212, sharex=ax1)
ax2.plot(t3,l0ltr,'b.', t1, l1ltr, 'ro', t5, l2ltr, 'k-')
plt.show()