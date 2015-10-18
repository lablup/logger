#! /bin/bash
export PYENV_ROOT="/logger/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv shell 3.5.0
# aiobotocore does not have pip distribution yet.
cd /logger
pip3 install git+https://github.com/jettify/aiobotocore.git@master
python3 setup.py install
pyenv rehash
