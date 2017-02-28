var WebSocketServer = require('ws').Server;
var zmq = require('zmq');
var client_img = zmq.socket('sub');
var client_txt = zmq.socket('sub');
var exec = require('child_process').exec;

var receiver_img = new WebSocketServer({
    port: 9900
});
var receiver_txt = new WebSocketServer({
    port: 9901
});

receiver_img.on('connection', function connection(ws) {
    ws.on('message', function incoming(message) {
        console.log("received:", message);
    });

    //receives stream
    client_img.on('message', function(data) {
        try {
            //send image to webpage
            ws.send(data, {
                binary: true
            });
        } catch (Exception) {
            console.log('Error: image not delivered to client:', Exception);
        }
    });
});

receiver_txt.on('connection', function connection(ws) {
    ws.on('message', function incoming(message) {
        console.log("received:", message);
    });
    client_txt.on('message', function(data) {
        try {
            //send image to webpage
            ws.send(data, {
                binary: false
            });
        } catch (Exception) {
            console.log('Error: message not delivered to client:', Exception);
        }
    });
});

client_img.connect('tcp://127.0.0.1:5000');
client_txt.connect('tcp://127.0.0.1:5001');
client_img.subscribe('');
client_txt.subscribe('');
