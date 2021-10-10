import RPi.GPIO as GPIO
from time import sleep

human_pin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(human_pin, GPIO.IN)

try:
    while True:        
        human = GPIO.input(human_pin)
        print(human)
        sleep(1)

except KeyboardInterrupt:
        pass

GPIO.cleanup()

