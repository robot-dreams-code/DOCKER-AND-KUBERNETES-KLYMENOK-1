FROM php:8.1.33

RUN mkdir -p /out
COPY exec.php /var/www/exec.php

ENTRYPOINT ["php", "/var/www/exec.php"]
CMD ["2", "4"]
