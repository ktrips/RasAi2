### Add programs to hotword.py ###

### A1 START ###

import time
import RPi.GPIO as GPIO

LED1   = 16
LED2   = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setwarnings(False)

import re
import os

### A1 END ###


### A2 START ###


            # Add the following lines after the existing line above:
            if command == "com.acme.commands.blink_light": #com.example.commands.BlinkLight":
                number = int( params['number'] )
                print(params['lightKey'])
                for i in range(int(number)):
                    print('Device is blinking.')
                    GPIO.output(LED1, GPIO.HIGH)
                    GPIO.output(LED2, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(LED1, GPIO.LOW)
                    GPIO.output(LED2, GPIO.LOW)
                    time.sleep(1)

### A2 END ###



### A3 START ###

            # Add motor commands after the existing line above:
            if command == "com.acme.commands.motor":
                direction = params['directionKey']
                print(direction)
                d = {"前":"forward", "後":"back", "右":"right", "左":"left"}
                for k,v in d.items():
                    if re.match(k, direction):
                        direct_command = v
                        break
                    else:
                        direct_command = "forward"

                print('Robot is moving '+direct_command)
                GPIO.output(LED1, GPIO.HIGH)
                GPIO.output(LED2, GPIO.HIGH)
                os.system('python motor2.py '+direct_command+' 3')
                GPIO.output(LED1, GPIO.LOW)
                GPIO.output(LED2, GPIO.LOW)

### A3 END ###

