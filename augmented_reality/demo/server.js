var WebSocketServer = require('ws').Server;
var zmq = require('zmq');
var client = zmq.socket('sub');
var exec = require('child_process').exec;

var receiver = new WebSocketServer({port: 9900});
receiver.on('connection', function connection(ws) {
    ws.on('message', function incoming(message) {
        //var msg = JSON.parse(message);
        console.log("received:", message);
    });

    //receives stream
    client.on('message', function(data) {
        try {
            //send stream to webpage
            ws.send(data, {binary:true});
        }
        catch(Exception) {
            console.log('Error: message not delivered to client:', Exception);
        }
    });
});
client.connect('tcp://127.0.0.1:5000');
client.subscribe('');
