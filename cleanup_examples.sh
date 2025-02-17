#!/usr/bin/env bash
set -Eeuxo pipefail

HOSTNAME=$(hostname)
USER=$(whoami)

FILES=('README.rst' 'examples.ipynb')

for file in "${FILES[@]}" ; do
    sed -i "s|${USER}|user|" "${file}"
    sed -i "s|${HOSTNAME}|hostname|" "${file}"
done
