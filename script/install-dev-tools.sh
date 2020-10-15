#!/usr/bin/env bash

# Install Git
apt-get install -y git 

# Install NPM - (from https://github.com/nodesource/distributions/blob/master/README.md)
apt-get install -y curl 
curl -sL https://deb.nodesource.com/setup_12.x | bash -
apt-get install -y nodejs

# Install Redis Cli
apt-get install -y redis

pip install -r requirements.txt
pip install -r requirements-dev.txt
