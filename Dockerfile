FROM ubuntu:20.04

COPY requirements.txt /mnt/requirements.txt
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nano x11vnc xvfb xfce4 xfce4-terminal dbus-x11 python3 python3-tk python3-pip && \
    apt-get autoclean && \
    apt-get autoremove && \
    pip3 install -r /mnt/requirements.txt && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p ~/.vnc && \
    x11vnc -storepasswd 1234 ~/.vnc/passwd && \
    echo "#!/bin/bash\nxrdb /root/.Xresources\nstartxfce4 &\nxfwm4 --replace\n" > ~/.vnc/xstartup && \
    chmod +x ~/.vnc/xstartup
COPY main.py /mnt/main.py

WORKDIR /mnt/
CMD ["x11vnc", "-forever", "-create"]
#CMD ["python3", "main.py"]
