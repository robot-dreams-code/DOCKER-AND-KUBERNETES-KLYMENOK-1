const http = require('http');
const { createClient } = require('redis');

const APP_STORE = process.env.APP_STORE || 'memory';
const REDIS_URL = process.env.APP_REDIS_URL || 'redis://redis:6379';

let redisClient = null;

async function initRedis() {
  if (APP_STORE !== 'redis') {
    console.log('Starting without Redis (APP_STORE != redis)');
    return;
  }

  try {
    redisClient = createClient({
      url: REDIS_URL,
    });

    redisClient.on('error', (err) => {
      console.error('Redis Client Error', err);
    });

    await redisClient.connect();
    console.log('Connected to Redis:', REDIS_URL);
  } catch (err) {
    console.error('Failed to connect to Redis:', err);
  }
}

const server = http.createServer(async (req, res) => {
  if (req.url === '/health') {
    res.writeHead(200);
    res.end('Ok');
    return;
  }

  let visits = 'N/A';

  if (APP_STORE === 'redis' && redisClient) {
    try {
      // збільшуємо лічильник звернень
      visits = await redisClient.incr('visits');
    } catch (err) {
      console.error('Error working with Redis:', err);
    }
  }

  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end(`Hello from course-app:lesson-11\r\nVisits: ${visits}\r\n`);
});

initRedis().then(() => {
  server.listen(8080, () => console.log('Server running on port 8080'));
});
