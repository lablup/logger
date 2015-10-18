#! /bin/bash
export PYENV_ROOT="/logger/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv shell 3.5.0
export PYTHONUNBUFFERED=1
run-logger -f /logger/conf/logger.conf
