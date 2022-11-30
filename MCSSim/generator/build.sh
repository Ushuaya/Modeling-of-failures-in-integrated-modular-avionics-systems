#!/bin/bash

make -f makefile.txt
cmake CMakeLists.txt
rm -r generated_components
mkdir generated_components
python network_generator.py ../models/
cd ..
make
