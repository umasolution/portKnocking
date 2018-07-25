# Owner : Jayesh Patel 
# jay.net.in@gmail.com
# Port Knocking is a way by which you can defend yourself against port scanners., it refuses access to a protected port until a client accesses a  sequence of other ports in the right order upfront.

import sys
import argparse
import time
import socket
import select
import time


class portKnock(object):
    def __init__(self, targetIP, targetPort, knockPortFile, protocol):
	self.targetIP = targetIP
	self.knockPortFile = knockPortFile	
	self.protocol = protocol
	self.targetPort = int(targetPort)

	print self.protocol

 
    def genPortList(self):
	with open("%s" % self.knockPortFile) as portList:
		knockPortList = portList.read().splitlines()
		return knockPortList


    def knock(self):
	pList = self.genPortList()

	for port in pList:
		for p in  port.split(','):
			result = self.sConnect(int(p))	
		
		status = self.connectVerify()
		if "Error" not in status:
			print "Port Knock Successfully Completed with %s, Now You can access %s port in this machine" % (port, self.targetPort)
			print "Note :"
			p1 = port.split(',')
			p1.reverse()
			print "To delete knock port run command : nc -nv %s %s" % (self.targetIP, ' '.join(p1)) 
			sys.exit(0)
		else:
			print "Testing Port Sequence %s : FAIL" % port



    def sConnect(self, port):
	try:
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.connect((self.targetIP, port))
	    s.settimeout(5.0)
	except socket.error:
	    return "Next"

    def connectVerify(self):
	check = "False"
	try:
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.settimeout(5.0)
	    s.connect((self.targetIP, self.targetPort))
	    check = s.recv(1024)
	    if "False" not in check:
	    	return check
	    else:
		return "Error"
	except socket.error:
	    if "False" not in check:
		return check
	    else:
		return "Error"

	   



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Pass Argument')
	parser.add_argument('targetIP', type=str, metavar='Target IP', help='Enter Target IP')
	parser.add_argument('targetPort', type=str, metavar='Target Service Port', help='Enter Targe Service Port')
	parser.add_argument('knockPortFile', type=str, metavar='Knock Ports File Name', help='Enter knock ports File Name')
	parser.add_argument('protocol', type=str, metavar='protocol name', help='Enter protocol name (TCP/UDP)')

	args = parser.parse_args()

	res = portKnock(args.targetIP, args.targetPort, args.knockPortFile, args.protocol)
	print res.knock()
	

