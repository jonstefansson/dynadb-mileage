#!/usr/bin/env bash
# Preventing referencing undefined variables
set -o nounset
# Do not ignore failing commands
set -o errexit

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source "${script_dir}/base.sh"

ddb list-tables | jq '.'
