var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var bodyParser = require('body-parser');

app.use(bodyParser.text({type:"*/*"}));

var authError = false;

app.post("/events/:name", function(req, res, next) {
    io.sockets.emit(req.params.name, req.body);
    res.send({});
});

app.post("/killSockets", function(req, res, next) {
    Object.keys(io.sockets.sockets).forEach(function(s) {
        io.sockets.sockets[s].disconnect(true);
    });

    res.send({});
});

app.post("/authError/:val", function(req, res, next) {
    authError = (req.params.val == 'true');

    res.send({authError});
});

io.on('connection', function(socket){
    console.log('a user connected');

    socket.on('disconnect', function(){
        console.log('user disconnected');
    });
});

io.use(function(socket, next) {
    if (authError === true) {
        next(new Error('Not Authorized'));
    }
    next();
});

io.on('error', function(socket){
    // Do nothing
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});