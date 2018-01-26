#!/usr/bin/env bash
start=${1:-30000}
./venv/bin/python dynadb-mileage.py query $start
