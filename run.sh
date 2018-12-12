#!/bin/bash -e

# Build it
docker build -t moose .

# Run the game, mounting the current X11 display
docker run -it \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --device /dev/snd \
    moose
