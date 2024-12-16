const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const motionSensor = require('./motionSensor');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// ...existing code...

motionSensor.on('motionDetected', () => {
    io.emit('motionDetected');
});

// ...existing code...

server.listen(3000, () => {
    console.log('Server is running on port 3000');
});
