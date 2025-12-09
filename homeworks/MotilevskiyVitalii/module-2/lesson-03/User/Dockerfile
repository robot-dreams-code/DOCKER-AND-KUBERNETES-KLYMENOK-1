FROM php:8.1.33

RUN useradd -u 10001 -m -s /bin/rbash app \
 && install -d -o app -g app /work

WORKDIR /work
USER app

EXPOSE 8080

CMD ["php", "-S", "0.0.0.0:8080", "-t", "/work"]
