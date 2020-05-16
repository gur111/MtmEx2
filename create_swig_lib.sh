#!/bin/bash

set -e
PY_INCLUDE_PATH=$(python3 -c "from sysconfig import get_paths as gp; print(gp()['include'])")
swig -python Olympics.i
gcc -std=c99 -fPIC -c Olympics_wrap.c -I${PY_INCLUDE_PATH}
ld -shared Olympics.o Olympics_wrap.o -L${PY_INCLUDE_PATH}/ -o _Olympics.so