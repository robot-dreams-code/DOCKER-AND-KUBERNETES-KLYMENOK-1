#!/bin/sh
echo "<h1>Container:${INDEX} - is alive!</h1>" > /usr/share/nginx/html/index.html

# Start Nginx in the foreground (so the container stays alive)
nginx -g 'daemon off;'
