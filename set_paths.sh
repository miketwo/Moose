#!/bin/bash

# This script finds internal python modules and creates a .pth file suitable
# for development. This allows us to eliminate many python system path
# hacks. Note that we do not use "setup.py develop" because this will attempt
# to install all of our requirements, which will install many packages from the
# pip repo that we would prefer to come from right here in the cosmogia repo.

TOP=$(cd $(dirname $0) && pwd)
PTH=/usr/local/lib/python2.7/dist-packages/moose.pth

echo "${TOP}/gamelib" > ${PTH}

# find ${TOP} -path ${TOP}/ -prune -o -name setup.py -printf "%h\n" > ${PTH}
