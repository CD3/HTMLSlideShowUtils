#! /bin/bash

set -e
mkdir $0.d
cd $0.d
../../setup.sh
cd demo
make
firefox html/00-slides.html
