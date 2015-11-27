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
			t.append(float(line[0]))
			v.append(float(line[1]))

ax1 = plt.subplot(311)
ax1.plot(t,v,'b-')

t = []
v = []
flag = True
with open("results/l1_bufferoccupancy_right-to-left.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t.append(float(line[0]))
			v.append(float(line[1]))

ax2 = plt.subplot(312, sharex=ax1)
ax2.plot(t,v,'r-')




plt.figure()

t = []
lostpackets = []
flag = True
with open("results/f1_src_packetloss.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t.append(float(line[0]))
			lostpackets.append(float(line[1]))

ax1 = plt.subplot(212)
ax1.plot(t,lostpackets,'bx-')

t = []
flowstate = []
flag = True
with open("results/f1_src_flowstate.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t.append(float(line[0]))
			flowstate.append(float(line[1]))

ax1.plot(t,flowstate,'r-')	
plt.ylim([0, 4])

t = []
windowsize = []
flag = True
with open("results/f1_src_windowsize.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t.append(float(line[0]))
			windowsize.append(float(line[1]))
ax2 = plt.subplot(211, sharex=ax1)
ax2.plot(t,windowsize,'k-')
plt.ylim([0,4])

t = []
out = []
left = []
in_transit = []
ackd = []
total = []
flag = True
with open("results/f1_src_outstandingpackets.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t.append(float(line[0]))
			out.append(float(line[1]))
			left.append(float(line[2]))
			in_transit.append(float(line[3]))
			ackd.append(float(line[4]))
			total.append(float(line[5]))

ax2.plot(t,out,'r-')
ax2.plot(t,left,'b-')
ax2.plot(t,in_transit,'r--')
ax2.plot(t,ackd,'b--')
ax2.plot(t,[in_transit[i]+ackd[i]+left[i] for i in xrange(len(t))],'ro')
ax2.plot(t,[out[i]+ackd[i]+left[i] for i in xrange(len(t))],'b.')
ax2.plot(t,total,'kx')

ax2.legend(('window','out', 'left', 'transit', 'ackd', 'total_t', 'total_o', 'total'), 'upper right')
plt.ylim([0,201])

plt.show()