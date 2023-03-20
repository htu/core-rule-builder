#!/bin/zsh 
#
python setup.py sdist bdist_wheel
pip install ./dist/rulebuilder-0.1.0.tar.gz
