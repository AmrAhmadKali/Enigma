FROM alpine

RUN apk fetch &&\
    apk add --no-cache nginx nano minify &&\
    rm -rf /var/cache/apk/*

COPY config/default.conf /etc/nginx/http.d/
ADD src/ /srv/http/
RUN cd /srv/http/ && find js/ -type f \
        -name "*.js" ! -name "*.min.*" ! -name "vfs_fonts*" \
        -exec echo {} \; \
        -exec minify -o {} {} \; &&\
    find css/ -type f \
        -name "*.css" ! -name "*.min.*" \
        -exec echo {} \; \
        -exec minify --output {} {} \;
#CMD nginx && /bin/sh
EXPOSE 80
CMD nginx -g 'daemon off;'
