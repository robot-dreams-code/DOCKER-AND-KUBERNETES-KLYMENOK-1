const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200);
    res.end('Ok');
    return;
  }
  res.writeHead(200);
  res.end('Hello from course-app:lesson-08');
});

server.listen(8080, () => console.log('Server running on port 8080'));
