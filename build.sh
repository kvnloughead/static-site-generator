#!/bin/bash
# Builds the project for deployment to GitHub Pages. The second argument will
# be used as the base path for deployment.

python3 src/main.py "/static-site-generator/" "./docs"