#!/bin/bash --rcfile
source /home/pi/env/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS=/home/pi/xxx.json
cd /home/pi/Programs/robot
python sensor_robot.py

