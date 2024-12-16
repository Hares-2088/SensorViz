const EventEmitter = require('events');
const motionSensor = new EventEmitter();

// ...existing code...

motionSensor.on('motionDetected', () => {
    console.log('Motion detected!');
    // ...existing code to handle motion detection...
});

// Simulate motion detection
setInterval(() => {
    motionSensor.emit('motionDetected');
}, 5000);

module.exports = motionSensor;
