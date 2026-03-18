FROM nginx:latest

RUN apt-get update && \
    apt-get install -y openssl && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/nginx && \
    mkdir -p /var/lib/nginx/tmp && \
    mkdir -p /etc/nginx/certs/ && \
    rm /etc/nginx/conf.d/default.conf && \
    chmod -R 644 /etc/nginx/certs/

COPY conf/app.conf /etc/nginx/conf.d/
COPY conf/nginx.conf /etc/nginx/

RUN openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
    -keyout /etc/nginx/certs/key.pem \
    -out /etc/nginx/certs/cert.pem \
    -subj "/C=BR/ST=MG/L=Lavras/O=App/CN=localhost"

EXPOSE 443
