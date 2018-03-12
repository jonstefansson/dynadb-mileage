#!/bin/bash
# -----------------------------------------------------------------------------
# Always source this file (do not execute it). It needs to change current 
# shell that you are working in.
# -----------------------------------------------------------------------------
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ ! -d "$script_dir/venv" ]]; then
    virtualenv --python=python3.6 "$script_dir/venv"
    echo "export PYTHONPATH=$script_dir" >> $script_dir/venv/bin/activate
fi
source venv/bin/activate
if [[ -f "$script_dir/requirements.txt" ]]; then
  pip3 install -r "$script_dir/requirements.txt"
fi
