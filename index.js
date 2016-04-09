const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const pythonShell = require('python-shell');
const port = process.env.PORT || 3000;

app.use((req, res) => {
  if(req.url == "/") {
    res.sendFile(__dirname + '/index.html');
  } else if (req.url == "/testSum") {
    const shell = new pythonShell('testSum.py');
    shell.on('message', (msg) => {
      console.log("message: " + msg);
      res.send(msg);
    });
    console.log("send: 1\n");
    shell.send("1")
    console.log("send: 2\n");
    shell.send("2");
  }
});

io.on('connection', (socket) => {
  console.log("a user connected");

  //Get a new drink when requested
  socket.on('GET_NEW_DRINK', () => {
    const shell = new pythonShell('testSum.py');
    shell.on('message', (msg) => {
      console.log("message: " + msg);
      io.emit('NEW_DRINK', msg);
    })
    shell.send(Math.floor((Math.random() * 10) + 1));
    shell.send(Math.floor((Math.random() * 10) + 1));
  });

  socket.on('disconnect', () => {
    console.log("a user disconnected");
  });
});

http.listen(port, () => {
  console.log("Site running on port " + port);
});
