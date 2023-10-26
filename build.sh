#!/bin/bash

#install dependencies
pip install -r build.sh

# Run Migrations
python jj.py migrate
