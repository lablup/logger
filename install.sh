#! /bin/bash
export PYENV_ROOT="/logger/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv shell 3.5.0
python3 /logger/setup.py install --upgrade
pyenv rehash
