FROM php:8.1.33 AS builder

ARG A
ARG B
LABEL authors="vitalii motilevskiy"

RUN test -n "$A" && test -n "$B" || (echo "ERROR: you must provide --build-arg A and B" >&2 && exit 1)

RUN useradd -u 10001 -m -s /usr/sbin/nologin app \
 && install -d -o app -g app /out

COPY --chown=app:app exec.php /var/www/exec.php

USER app

RUN mkdir -p /out \
 && php /var/www/exec.php "$A" "$B" /out/result.txt \
 && ls -l /out/result.txt

FROM scratch

COPY --from=busybox:1.37.0-musl /bin/busybox /bin/busybox
COPY --from=builder /out/result.txt /result.txt

USER 10001:10001

EXPOSE 8080

ENTRYPOINT ["/bin/busybox", "cat", "/result.txt"]
