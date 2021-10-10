#!/bin/bash --rcfile
source /home/pi/env/bin/activate
cd /home/pi/Programs
echo "Google Hotword Robot is running!"
python led3.py
python hotword_robot.py
echo "Hotword is completed!"
