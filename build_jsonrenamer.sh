#!/bin/zsh 
#
python setup_jsonrenamer.py sdist bdist_wheel
pip install ./dist/jsonrenamer-0.1.0.tar.gz
