#!/bin/bash

set -e

unoconv -l &

python3 -m printathpi.app
