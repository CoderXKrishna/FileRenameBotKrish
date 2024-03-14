#!/bin/bash

# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it and try again."
    exit 1
fi

# Check if bot.py is present in the current directory
if ! [ -f bot.py ]
then
    echo "bot.py is not present in the current directory. Please place it here and try again."
    exit 1
fi

# Run the worker
python3 bot.py
