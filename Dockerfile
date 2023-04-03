FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV HOME /home/developer

COPY requirements.txt /mnt/requirements.txt
RUN apt-get update &&\
    apt-get install -y python3 python3-pip &&\
    apt-get install -y python3-tk &&\
    pip install -r /mnt/requirements.txt && \
    apt-get purge -y python3-pip &&\
    apt-get autoremove -y &&\
    rm -rf /var/lib/apt/lists/*

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    useradd developer &&\
    usermod -aG sudo developer &&\
    chown ${uid}:${gid} -R $HOME

USER developer
COPY main.py $HOME
WORKDIR $HOME
CMD /usr/bin/python3 main.py
