#!/bin/bash -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd $DIR
apt-get update
apt-get install -y $(grep -vE "^\s*#" apt-requirements.txt  | tr "\n" " ")
apt-get build-dep -y python-pygame
pip install -U pip
pip install -r requirements.txt
