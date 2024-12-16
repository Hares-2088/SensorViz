const socket = io();

// ...existing code...

socket.on('motionDetected', () => {
    alert('Motion detected!');
    // Update the dashboard view as needed
});
