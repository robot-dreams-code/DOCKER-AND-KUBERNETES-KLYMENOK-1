FROM nginx:alpine

COPY insert_html.sh /insert_html.sh
RUN chmod +x /insert_html.sh

# Expose Nginx HTTP port
EXPOSE 80

CMD ["/insert_html.sh"]