#! /bin/bash
export PYENV_ROOT="/logger/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv shell 3.5.0
cd /logger
# aiobotocore does not have pip distribution yet.
pip3 install git+https://github.com/jettify/aiobotocore.git@master
pip3 install ./logger-0.1.0-py3-none-any.whl
pyenv rehash
