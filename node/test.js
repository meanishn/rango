var http=require('http');
var server=http.createServer().listen(8002);
var io=require('socket.io').listen(server);
var cookie_reader = require('cookie');
var redis=require('redis');

io.use(function(socket,next){
    handshakeData=socket.request;
    
    if (handshakeData.headers.cookie){
        socket.handshake.cookie= cookie_reader.parse(handshakeData.headers.cookie);
        
        return next();}
    
    next(new Error('Authentication error'));
    
    });
    
io.on('connection', function(socket){
    console.log('connected');
    var client=redis.createClient();
    
    client.subscribe('category-'+ socket.handshake.cookie['sessionid']);
    client.on('error', function(err){
        console.log("Error " + err);
    });

    client.on('message', function(channel, message){
        console.log('channel-'+ channel+ ' '+ message);
        io.emit(channel, message);
    });
    
    socket.on('disconnect', function(){
        console.log('disconnected');
        client.unsubscribe('category-'+ socket.handshake.cookie['sessionid']);
    });
});
