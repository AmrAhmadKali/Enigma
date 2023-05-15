FROM alpine

RUN apk fetch &&\
    apk add nginx nano &&\
    rm -rf /var/cache/apk/*

COPY config/default.conf /etc/nginx/http.d/
ADD src/ /srv/http/
#CMD nginx && /bin/sh
EXPOSE 80
CMD nginx -g 'daemon off;'
