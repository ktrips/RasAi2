# -*- encoding:utf-8 -*-

from tkinter import *
from datetime import datetime
import RPi.GPIO as GPIO
from time import sleep

import urllib
import json
from io import BytesIO
from PIL import Image, ImageDraw
import math
import os

import sys
import subprocess
import requests
import yaml

url = 'https://raspiface.cognitiveservices.azure.com/face/v1.0/detect'
key = 'xxx'
ret = 'age,gender,smile,emotion'

human_pin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(human_pin, GPIO.IN)

def face_api(url, key, ret, image):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': key,
        'cache-control': 'no-cache',
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': ret,
    }
    data = open(image, 'rb').read()
    try:
        jsnResponse = requests.post(url ,headers=headers, params=params, data=data)
        if(jsnResponse.status_code != 200):
            jsnResponse = []
        else:
            jsnResponse = jsnResponse.json()
    except requests.exceptions.RequestException as e:
        jsnResponse = []

    return jsnResponse

def camera():
    now = datetime.now()
    dir_name = now.strftime('%Y%m%d')
    dir_path = '/home/pi/Programs/image/' + dir_name + '/'
    file_name= now.strftime('%H%M%S') + '.jpg'
    fname    = dir_path + file_name
    try:
        os.mkdir(dir_path)
    except OSError:
        print('Date dir already exists')
    os.system('sudo raspistill -h 640 -w 480 -o ' + fname)
    return fname

def call_face(fname):

    faces = face_api(url, key, ret, fname)
    print('3. Run Face API!')

    if faces:
        for face in faces:
          left  = face["faceRectangle"]["left"]
          top   = face["faceRectangle"]["top"]
          right = face["faceRectangle"]["left"]+face["faceRectangle"]["width"]
          bottom= face["faceRectangle"]["top"]+face["faceRectangle"]["height"]
          age   = math.floor(face["faceAttributes"]["age"])
          gender= face["faceAttributes"]["gender"]
          print(left, top, right, bottom, age, gender)

          if age < 20:
                  if gender == 'male':
                    category = 'Boy'
                  else:
                    category = 'Girl'
          else:
                  if gender == 'male':
                    category = 'Man'
                  else:
                    category = 'Woman'
          face_result = category+" ("+gender+", "+str(age)+")"
          print ('5. Result: '+face_result)
         
          os.system('omxplayer -o hdmi /home/pi/Programs/image/'+category+'.mp4') #h264')

    else:
        print('4. No face detected')

    return face_result

# メインウィンドウ作成
root = Tk()
# メインウィンドウサイズ
root.geometry("720x480")
# メインウィンドウタイトル
root.title("PiDisplay")

# Canvas 作成
c = Canvas(root, bg="#FFFFFF", width=500, height=480)
c.pack(expand=True, fill='x', padx=5, side='left')
#r = Canvas(root, bg="#FFFFFF", width=200, height=480)
#r.pack(expand=True, fill='x', padx=5, side='right')
QR = "/home/pi/Programs/image/qr.gif"

# 文字列作成
ch = c.create_text(350, 80, font=('', 60, 'bold'), fill='red')
cd = c.create_text(350, 180, font=('', 40, 'bold'), fill='black')
ct = c.create_text(350, 280, font=('', 80), fill='black')
cf = c.create_text(350, 400, font=('', 40), fill='blue')
img = PhotoImage(file=QR)
Label(root, image = img).pack(side='right', padx=5)

# メインウィンドウの最大化
root.attributes("-zoomed", "1")
# 常に最前面に表示
root.attributes("-topmost", False)

def cupdate():
    """hpin=GPIO.input(human_pin)
    if hpin == 1:
        h='人が来ました！' #'Human Detected'
    else:
        h='誰もいません' #'No Human'
    print(h)"""

    human_exists = int(GPIO.input(human_pin) == GPIO.HIGH)
    if human_exists:
        stext = '人が来ました！'
        print('1. Human exists!')
        fname = camera()
        print('2. Took a picture as '+fname)
        if fname:
          face_result = call_face(fname)
          stext = face_result
        else:
          print('2. No picture taken')
    else:
       stext = '誰もいません'
       print('0. No human')
    sleep(1)

    # 現在時刻を表示
    now = datetime.now()
    d = '{0:0>4d}年{1:0>2d}月{2:0>2d}日 ({3})'.format(now.year, now.month, now.day, now.strftime('%a'))
    t = '{0:0>2d}:{1:0>2d}:{2:0>2d}'.format(now.hour, now.minute, now.second)
    c.itemconfigure(ch, text='Pi Display')
    c.itemconfigure(cd, text=d)
    c.itemconfigure(ct, text=t)
    c.itemconfigure(cf, text=stext)
    c.update()
    # 1秒間隔で繰り返す
    root.after(1000, cupdate)

# コールバック関数を登録
root.after(1000, cupdate)
# メインループ
root.mainloop()

GPIO.cleanup()
