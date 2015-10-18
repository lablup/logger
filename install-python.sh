#! /bin/bash
export PYENV_ROOT="/logger/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv install 3.5.0
