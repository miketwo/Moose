#!/bin/bash

docker build -t game .

ARG=${1:-/bin/bash}

# Run it, mounting the code so that changes are reflected inside the container.
docker run -it \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $(pwd):/app \
    game $ARG
