import sys
import zmq
import json
import ast

#python2.7 router.py 12345 [[1,2,3],[4,5]] '[6]' '[5002, 5003, 5004]' false
#            0         1           2         3          4                5	


#Sharding Function
def getGroup(customerID, numGroups):
	return hash(customerID) % numGroups;

context = zmq.Context()
#All clusterNodes will send their packets to this socket
receiver_socket = context.socket(zmq.PULL)
receiver_socket.bind("tcp://*:"+str(sys.argv[1]))

#All clusterNodes will receive packets from this socket
sender_socket = context.socket(zmq.PUB)
sender_socket.bind("tcp://*:5000");


#NodeIds of all clusterServers
groups = ast.literal_eval(sys.argv[2]) #list of lists
numGroups = len(groups)
servingIndices = [0] * numGroups

#NodeIds of all webServers (currently only one webServer supported)
webServers = ast.literal_eval(sys.argv[3])
webServers = [str(x) for x in webServers]
clusterServerId = 0

#WebServer receives response from this socket
#Port numbers of all webServers on which they will listen
webServersPortNos = ast.literal_eval(sys.argv[4])
print webServersPortNos	
webServersPortNos = [str(x) for x in webServersPortNos]
port_dict = {}
if len(webServersPortNos) != len(webServers):
	print "Number of port numbers doesn't match number of webservers!\n"
	exit()

for i in range(len(webServers)):
	socket = context.socket(zmq.PUSH)
	socket.bind("tcp://*:"+webServersPortNos[i])
	port_dict[webServers[i]] = socket



#Whether to print
debug = (sys.argv[5] == "true")

if debug:
	print "Groups = ", groups
	print "webServers = ", webServers

while True:
	data = receiver_socket.recv_json()
	dest_id = str(data.get('dest'))
	#if debug:
	#	print data
	#print dest_id
	if dest_id == 'None': 
		#Packet received from a webserver
		#We don't know the destination
		#Find group from customerId
		#Assign in a round robin fashion in the group
		customerId = data['customerId']
		groupId = getGroup(customerId, numGroups)
		dest_id = str(groups[groupId][servingIndices[groupId]])
		print "Serving to group %d and destination %s"%(groupId, dest_id)
		servingIndices[groupId] = (servingIndices[groupId]+1)%(len(groups[groupId]))
	if dest_id not in webServers:
		sender_socket.send("%s %s"%(dest_id, data))
	else:
		print data
		port_dict[dest_id].send("%s"%(json.dumps(data)))
