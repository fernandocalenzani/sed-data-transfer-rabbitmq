#!/bin/bash

python consumer/__main__.py &

#python producer/__main__.py &

python ai/__main__.py

exec tail -f /dev/null
