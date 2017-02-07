FROM nginx

MAINTAINER CIRX Software, cirxsoftware@gmail.com

# Copy NGINX config
COPY ./docker/nginx/nginx_wekker.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/mime.types /etc/nginx/mime.types

# Copy SSL Certificates
COPY ./docker/nginx/certificates /certificates

# Copy Frontend Project
COPY ./dist /usr/share/nginx/html