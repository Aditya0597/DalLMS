const bodyParser = require('body-parser')
const express = require('express');
const dotenv = require('dotenv')
dotenv.config()
const MessageController = require('./src/controller/MessageController.js')

const app = express()
const http = require('http').Server(app);
const io = require('socket.io')(http);

const SERVER_PORT = process.env.PORT || 8080

app.set('view engine', 'ejs');

app.get('/', function (req, res) {

    console.log(req.get('host'));
    res.render('index.ejs', { host: req.get('host') });
});

app.get('/messageHistory', function (req, res) {
    let controller = new MessageController();
    controller.getMessages(req, res)
});


var userCount = 0;

io.sockets.on('connection', function (socket) {

    socket.on('user', function (user) {
        console.log(`user joinde the chat:  ${user}`)

        socket.username = user;
        io.emit('has_joined', '🟢🟢🟢 <strong> <i> ' + socket.username + ' has joinned the chatroom </i> </strong> ');
        
        userCount++

        console.log(`New user added to the chat room:${socket.username}`)
        console.log(`User count in the chat room: ${userCount}`)

        if (userCount == 1) {
            let controller = new MessageController()
            controller.createTopicAndSubscription()
        }
    });

    socket.on('disconnect', function (user) {
        io.emit('has_left', '🔴🔴🔴 <strong> <i>' + socket.username + ' has left the chatroom</i> </strong>');
        userCount--;

        console.log(`User : ${socket.username} has left the chat room`)
        console.log(`User count in the chat room: ${userCount}`)

        if (userCount == 0) {
            let controller = new MessageController()
            controller.saveUserChat()

        }
    })

    socket.on('chat_message', function (chatData) {
        io.emit('chat_message', '<strong>' + socket.username + '</strong>: ' + chatData);

        let data = {
            user: socket.username,
            message: chatData,
            time: new Date()
        }

        let controller = new MessageController()
        controller.publishMessage(data)
    });

});

const expressServer = http.listen(SERVER_PORT, function () {
    console.log(`Everything looks good. The LMS chat service has started on ${SERVER_PORT}`);
});