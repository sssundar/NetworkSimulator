import sys, os
import json
import matplotlib.pyplot as plt

# plt.figure()

# t = []
# v = []
# flag = True
# with open("results/l1_bufferoccupancy_left-to-right.txt") as m:   
# 	for line in m:
# 		if flag:
# 			flag = False			
# 		else:
# 			line = line.strip().split("\t\t")
# 			t.append(float(line[0]))
# 			v.append(float(line[1]))

# ax1 = plt.subplot(311)
# ax1.plot(t,v,'b-')

# t = []
# v = []
# flag = True
# with open("results/l1_bufferoccupancy_right-to-left.txt") as m:   
# 	for line in m:
# 		if flag:
# 			flag = False			
# 		else:
# 			line = line.strip().split("\t\t")
# 			t.append(float(line[0]))
# 			v.append(float(line[1]))

# ax2 = plt.subplot(312, sharex=ax1)
# ax2.plot(t,v,'r-')




# plt.figure()

# t = []
# lostpackets = []
# flag = True
# with open("results/f1_src_packetloss.txt") as m:   
# 	for line in m:
# 		if flag:
# 			flag = False			
# 		else:
# 			line = line.strip().split("\t\t")
# 			t.append(float(line[0]))
# 			lostpackets.append(float(line[1]))

# ax1 = plt.subplot(212)
# ax1.plot(t,lostpackets,'bx-')

# t = []
# flowstate = []
# flag = True
# with open("results/f1_src_flowstate.txt") as m:   
# 	for line in m:
# 		if flag:
# 			flag = False			
# 		else:
# 			line = line.strip().split("\t\t")
# 			t.append(float(line[0]))
# 			flowstate.append(float(line[1]))

# ax1.plot(t,flowstate,'r-')	
# plt.ylim([0, 4])

# t = []
# windowsize = []
# flag = True
# with open("results/f1_src_windowsize.txt") as m:   
# 	for line in m:
# 		if flag:
# 			flag = False			
# 		else:
# 			line = line.strip().split("\t\t")
# 			t.append(float(line[0]))
# 			windowsize.append(float(line[1]))
# ax2 = plt.subplot(211, sharex=ax1)
# ax2.plot(t,windowsize,'k-')
# plt.ylim([0,4])

# t = []
# out = []
# left = []
# in_transit = []
# ackd = []
# total = []
# flag = True
# with open("results/f1_src_outstandingpackets.txt") as m:   
# 	for line in m:
# 		if flag:
# 			flag = False			
# 		else:
# 			line = line.strip().split("\t\t")
# 			t.append(float(line[0]))
# 			out.append(float(line[1]))
# 			left.append(float(line[2]))
# 			in_transit.append(float(line[3]))
# 			ackd.append(float(line[4]))
# 			total.append(float(line[5]))

# ax2.plot(t,out,'r-')
# ax2.plot(t,left,'b-')
# ax2.plot(t,in_transit,'r--')
# ax2.plot(t,ackd,'b--')
# ax2.plot(t,[in_transit[i]+ackd[i]+left[i] for i in xrange(len(t))],'ro')
# ax2.plot(t,[out[i]+ackd[i]+left[i] for i in xrange(len(t))],'b.')
# ax2.plot(t,total,'kx')

# ax2.legend(('window','out', 'left', 'transit', 'ackd', 'total_t', 'total_o', 'total'), 'upper right')
# plt.ylim([0,201])


# plt.figure()

# t = []
# ws = []
# epit = []
# state = []
# flag = True
# with open("results/f1_src_fullrenodebug.txt") as m:   
# 	for line in m:
# 		if flag:
# 			flag = False			
# 		else:
# 			line = line.strip().split("\t\t")
# 			t.append(float(line[0]))
# 			epit.append(int(line[3]))
# 			ws.append(float(line[5]))
# 			state.append(10*int(line[14]))
# ax1 = plt.subplot(111)
# ax1.plot(t,ws,'b-',t,state,'r-',t,epit,'k-')

# plt.figure()


plt.figure()

t = []
ws = []
epit = []
state = []
rttmin = []
rttact = []
flag = True
with open("results/f1_src_fullvegasdebug.txt") as m:   
	for line in m:
		if flag:
			flag = False			
		else:
			line = line.strip().split("\t\t")
			t.append(float(line[0]))
			epit.append(int(line[3]))
			ws.append(float(line[5]))
			state.append(10*int(line[13]))
			rttmin.append(float(line[17]))
			rttact.append(float(line[18]))			
ax1 = plt.subplot(211)
ax1.plot(t,ws,'b-',t,state,'r-',t,epit,'k-')
ax2 = plt.subplot(212)
ax2.plot(t,rttmin,'b-',t,rttact,'r-')

# plt.figure()

# t = []
# ws = []
# epit = []
# rttmin = []
# rttmax = []
# rttact = []
# flag = True
# with open("results/f1_src_fulltruefastdebug.txt") as m:   
# 	for line in m:
# 		if flag:
# 			flag = False			
# 		else:
# 			line = line.strip().split("\t\t")
# 			t.append(float(line[0]))
# 			epit.append(int(line[3]))
# 			ws.append(float(line[5]))			
# 			rttmin.append(float(line[14]))
# 			rttmax.append(float(line[15]))
# 			rttact.append(float(line[16]))			
# ax1 = plt.subplot(211)
# ax1.plot(t,ws,'r-',t,epit,'k-')
# ax2 = plt.subplot(212)
# ax2.plot(t,rttmin,'b-',t,rttmax,'k-',t,rttact,'r-')

plt.figure()

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