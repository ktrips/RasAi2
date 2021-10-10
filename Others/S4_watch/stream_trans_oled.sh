#!/bin/bash --rcfile
source /home/pi/env/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS=/home/pi/xxx.json
cd /home/pi/Programs/
echo "Stream Trans is running!"
python stream_trans_oled.py
echo "Stream Translation is completed!"

