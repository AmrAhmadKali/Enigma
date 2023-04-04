FROM alpine
#ENV DEBIAN_FRONTEND=noninteractive
ENV HOME /home/developer

COPY requirements.txt /mnt/requirements.txt
RUN apk fetch &&\
    apk add python3 python3-tkinter py3-pip &&\
    pip install -r /mnt/requirements.txt &&\
    rm -rf /var/cache/apk/* &&\
    apk del py3-pip &&\
    rm -rf /usr/share


# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    adduser developer -D &&\
    chown ${uid}:${gid} -R $HOME

#USER developer
COPY main.py $HOME
WORKDIR $HOME
#CMD /bin/sh
CMD python3 main.py
