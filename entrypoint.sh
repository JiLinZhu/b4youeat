#!/bin/bash

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="localenv"

pyenv local 3.12.3

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python -m venv $VENV_DIR
fi



source $VENV_DIR/bin/activate

pip install -r requirements.txt > /dev/null 2>&1

export PYTHONPATH="$DIR/b4youeat:$PYTHONPATH"

exec $SHELL