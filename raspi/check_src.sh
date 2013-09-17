#!/bin/bash
for f in src/*.py 
do
  python -m py_compile $f
done
