// For use in tox.ini some day: npm --prefix ./tests/mock_server install ./tests/mock_server

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var bodyParser = require('body-parser');

app.use(bodyParser.text({type:"*/*"}));

var authError = false;

app.post("/events/:name", function(req, res, next) {
    io.sockets.emit(req.params.name, req.body);
    res.send();
});

app.post("/killSockets", function(req, res, next) {
    Object.keys(io.sockets.sockets).forEach(function(s) {
        io.sockets.sockets[s].disconnect(true);
    });

    res.send();
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

var server = http.listen(3000, function(){
  console.log('listening on *:3000');
});

var gracefulShutdown = function() {
  console.log("Received kill signal, shutting down gracefully.");
  server.close(function() {
    console.log("Closed out remaining connections.");
    process.exit()
  });
  
   // if after 
   setTimeout(function() {
       console.error("Could not close connections in time, forcefully shutting down");
       process.exit()
  }, 3*1000);
}

// listen for TERM signal .e.g. kill 
process.on ('SIGTERM', gracefulShutdown);

// listen for INT signal e.g. Ctrl-C
process.on ('SIGINT', gracefulShutdown);   


app.post("/shutdown", function(req, res, next) {
    setTimeout(function() {
      gracefulShutdown();
    }, 1*1000);
    
    res.send();
});