#!/usr/bin/env python
import skywriter
import signal
import os

from gpiozero import Motor
import time
import sys

motor = Motor(forward=20, backward=21) 
second = 3
some_value = 5000

@skywriter.flick()
def flick(start,finish):
  print('Got a flick!', start, finish)
  if start == "north" and finish == "south":
      print('Go forward '+str(second))
      motor.forward(0.5)
      time.sleep(second)
      motor.stop()

  elif start == "south" and finish == "north":
      print('Back ward '+str(second))
      motor.backward(0.5)
      time.sleep(second)

  motor.stop()

@skywriter.airwheel()
def spinny(delta):
  global some_value
  some_value += delta
  if some_value < 0:
  	some_value = 0
  if some_value > 10000:
    some_value = 10000
  print('Airwheel:', some_value/100)

@skywriter.double_tap()
def doubletap(position):
  print('Double tap!', position)
  os.system("python3 /home/pi/Programs/robot/pushtorobot.py --once")

@skywriter.tap()
def tap(position):
  print('Tap!', position)
  os.system('python3 /home/pi/Programs/robot/camera_detect.py labels')

@skywriter.touch()
def touch(position):
  print('Touch!', position)

signal.pause()