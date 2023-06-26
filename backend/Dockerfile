FROM alpine
ENV HOME /home/developer

RUN apk fetch &&\
    apk add python3 py3-pip &&\
    rm -rf /var/cache/apk/*

COPY requirements.txt $HOME/

RUN pip install -r $HOME/requirements.txt && apk del py3-pip && rm -rf /usr/share
# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    adduser developer -D &&\
    mkdir $HOME/data &&\
    chown ${uid}:${gid} -R $HOME/

USER developer
COPY main.py $HOME/
ADD meta $HOME/meta
ADD core $HOME/core
WORKDIR $HOME/
EXPOSE 25500
CMD python3 -ubEOO main.py
