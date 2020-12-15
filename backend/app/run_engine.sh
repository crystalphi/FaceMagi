#!/bin/bash

cd `dirname $0`/app/engine_v1
env SECRET_KEY="xyz123" python3 ./main.py

