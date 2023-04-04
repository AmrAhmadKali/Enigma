#!/bin/sh
docker build -t enigma .
xhost +local:root
docker run -ti --rm \
       -e DISPLAY=$DISPLAY \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       enigma
xhost -local:root

