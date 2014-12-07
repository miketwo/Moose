#!/bin/bash -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd $DIR
apt-get update
apt-get install -y $(grep -vE "^\s*#" apt-requirements.txt  | tr "\n" " ")
pip install -r requirements.txt
