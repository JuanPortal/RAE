#!/bin/bash

# Install CA certificates
apt-get update && apt-get install -y ca-certificates

# Run your bot
python3 main.py
