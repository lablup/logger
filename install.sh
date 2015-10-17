#! /bin/bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv install 3.5.0
pyenv shell 3.5.0
python3 setup.py install --upgrade --user
pyenv rehash
