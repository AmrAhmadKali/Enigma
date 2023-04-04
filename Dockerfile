FROM alpine
ENV HOME /home/developer/

RUN apk fetch &&\
    apk add python3 python3-tkinter py3-pip &&\
    rm -rf /var/cache/apk/*

COPY requirements.txt $HOME

RUN pip install -r $HOME/requirements.txt && apk del py3-pip && rm -rf /usr/share
# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    adduser developer -D &&\
    chown ${uid}:${gid} -R $HOME

USER developer
COPY main.py $HOME
ADD core/ $HOME/core
WORKDIR $HOME
#CMD /bin/sh
CMD python3 main.py
