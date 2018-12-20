//node clientServer.js 5 tcp://127.0.0.1 12345 true 3000 5002
//0       1            2          3        4     5    6    7

var app = require('express')();
var bodyParser = require('body-parser');
var formidable = require('express-formidable');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));
app.use(formidable());
var http = require('http').Server(app);
var zmq = require('zmq');


serverID = process.argv[2]
router_address = process.argv[3]
send_port_no = process.argv[4]
debug = (process.argv[5] == "true")
web_port = process.argv[6]
listen_portno = process.argv[7]


listen_socket = zmq.socket('pull');
listen_socket.connect(router_address+":"+listen_portno)

sender_socket = zmq.socket('push')
sender_socket.connect(router_address+":"+send_port_no)

var writePending_dict = [],
readPending_dict = [];


listen_socket.on('message', function(){

  // Parsing Message

  var args = Array.apply(null, arguments);
  console.log(args[0].toString('utf8'));
  var message = JSON.parse(args[0].toString('utf8'))
  console.log(message);
  if (message['dest'] != serverID)
    return;

  if (message['rpc'] == 'addEntryReply')
  	writePending_dict[message['requestId']] = message['status'];
  else if (message['rpc'] == 'readEntryReply'){
  	readPending_dict[message['requestId']] = message['data'];
  }

});


//For reading request
//Request Infromation:
//Post Request - multipart/formdata
//Keys - clientId, sourceId
app.post('/readData', function(req, res){
  var requestId = Math.random().toString(36).substring(7); //Assigning a randomID
  if (debug) console.log("Read RequestID assigned : " + requestId)
  readPending_dict[requestId] = 'failure';
  var data = req.fields;
  if (debug) console.log(data);
  var fileName = data['clientId']+"/"+data['sourceId'];
  msg = {'clientId' : serverID
  , 'requestId': requestId
  , 'rpc' : 'readEntry'
  , 'fileName' : fileName
  , 'customerId' : data['clientId']
  , 'sourceId' : data['sourceId']
  };
  sender_socket.send(JSON.stringify(msg));
  if (debug) console.log(msg);
  var count = 20;
  var my_int = setInterval(function(){
    if (count == 0){
      res.send("Server Timeout!");
      if (debug) "Request id " + requestId + "didn't got serve\n"
      clearInterval(my_int);
      return;
    }
    // count -= 1;
    if (readPending_dict[requestId] != "failure"){
      if (debug) console.log(readPending_dict[requestId]);
      res.send(readPending_dict[requestId]);
      clearInterval(my_int);
    }
  }, 100);
  return;
});


//For writing request
//Requests Information:-
//POST REQUEST - multipart/formdata
//Keys - fileData, clientId, sourceId
app.post('/pushData', function(req, res){
	var requestId = Math.random().toString(36).substring(7); //Assigning a randomID
	if (debug) console.log("Write RequestID assigned : " + requestId)
	writePending_dict[requestId] = 'failure';
  data = req.fields;
  if (debug) console.log(data)
  msg = {'clientId':serverID
  , 'requestId' : requestId
  , 'requestData' : {'fileData': new Date().getTime() + ":" + data['fileData'] + "\n", 'clientId': data['clientId'], 'sourceId':data['sourceId'] }
  , 'rpc':'addEntry'
  , 'customerId' : data['clientId']
  , 'sourceId' : data['sourceId']
  };
  sender_socket.send(JSON.stringify(msg));
  if (debug) console.log(msg)
  var count = 20;
  var my_int =   setInterval(function(){
    if (count == 0) {
    	res.send("Server Timeout!");
    	clearInterval(my_int);
  	  return;
    }
    // count -= 1;
    if (writePending_dict[requestId] == "Success"){
  	  if (debug) console.log("Log accepted");
  	  res.send("Log added!");
  	  clearInterval(my_int);
    }
  },100);
  return;
});


//Start http server
http.listen(web_port, function(){
  console.log('listening on *:3000');
});


