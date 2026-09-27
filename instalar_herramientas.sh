#!/usr/bin/env bash
# Descarga y compila Fast Downward y VAL, y descarga pddl-instances, en ../tools.
# Se usan las mismas versiones que en el experimento.
# Requisitos: git, cmake, g++, make y python3.
set -e
FD_COMMIT=9b81c7e422fdf7be9f73b96e9a7a969c483dd5d4
VAL_COMMIT=3c7a1f330bdab0ba28a4762bb45c3f06c27fb6d4
IPC_COMMIT=cf19edf7c53d1540ddbb396c642595e0926ee552

mkdir -p ../tools && cd ../tools
[ -d downward ] || git clone https://github.com/aibasel/downward.git
[ -d VAL ] || git clone https://github.com/KCL-Planning/VAL.git
[ -d pddl-instances ] || git clone https://github.com/potassco/pddl-instances.git
(cd downward && git checkout -q $FD_COMMIT && python3 build.py release)
(cd VAL && git checkout -q $VAL_COMMIT && mkdir -p build && cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j2)
(cd pddl-instances && git checkout -q $IPC_COMMIT)
