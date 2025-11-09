FROM busybox
WORKDIR /hello_world
COPY index.html .
EXPOSE 8080

CMD ["busybox", "httpd", "-f", "-p", "8080"]

