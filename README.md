# Cloud Haoma

The project was done in a team effort. Team Members:-
1. Supriya Aggarwal 2014A7PS0013P
2. Vidhi Jain 2014A7TS0113P
3. Abhishek Gupta 2014A7PS0026P

Run the following commands on all the nodes of the cluster

Python version 2.7

1. sudo apt-get install nodejs nodejs-legacy npm libzmq-dev git
2. pip install pyzmq-static
2. Open Terminal in the base directory of the project
3. npm install
4. pip install zmq


Network topology is star.

Run the following on the designated router.

1. python2.7 router.py 12345 [[1,2,3],[4,5]] '[6]' false


Run the following on the cluster nodes (you may include router also (Let IPADDRESS of router node for this be 127.0.0.1):-

Group I 
1. python2.7 server.py 1 tcp://127.0.0.1 12345 ["1","2","3"] on node1
2. python2.7 server.py 2 tcp://127.0.0.1 12345 ["1","2","3"] on node2
3. python2.7 server.py 3 tcp://127.0.0.1 12345 ["1","2","3"] on node3

Group II
1. python2.7 server.py 4 tcp://127.0.0.1 12345 ["4","5"] on node4
2. python2.7 server.py 5 tcp://127.0.0.1 12345 ["4","5"] on node5



Run the following code on the node which you want to run your web server
(Currently webserver tries to insert hardcoded values in the db on receiving
 the API call instead of using request Data)


1.node clientServer.js 6 tcp://127.0.0.1 12345 true 3000

API CALL:- 

IPADDRESSOFWEBSERVER:3000/readData


//For writing request
//Requests Information:-
//POST REQUEST - multipart/formdata
//Keys - fileData, clientId, sourceId

IPADDRESSOFWEBSERVER:3000/pushData


//For reading request
//Request Infromation:
//Post Request - multipart/formdata
//Keys - clientId, sourceId

IPADDRESSOFWEBSERVER:3000/readData




# Strategy
Using RAFT for log replication. 
Each log entry contains the write request by a client. Request contains sufficient 
information to identify the file. State machine operation is to append the request 
data to the identified file.
Reads can be handled by the leader
Data is sharded across the groups (here gropu I and II). Raft replicates the logs on all the nodes of the cluster => So if we run a single Raft instance for our cluster, we can't achieve a replication factor less than that of cluster size => Cluster should be divided into groups(shards) and raft instance should run for that group. => A data item will be present in one group only and replication is within the nodes of that group

Some consensus algorithms support partial replication in which we can control which data will replicated and its replication factor. Raft doesn't support it so we should shard our data to get decrease replication factor. Also, sharding improves writes throughput.

# Status
Code for supporting the write and read operation is working with the API Calls.

# Reference

This project is based on the raft implementation present at https://github.com/albertdb/Raft.

The entire code was rewritten into python (Original code was written in nodejs which
we suspect to be better choice than python because of its asynchronous nature)

ZeroMQ (http://zeromq.org/) is used for providing communication

