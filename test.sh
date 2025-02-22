#!/bin/bash

# -p pattern to match
# -s directory to start discovery
# -t directory containing tests (top level)
python3 -m unittest discover -s src -p "*test*.py" -t src