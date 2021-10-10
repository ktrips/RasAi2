# -*- encoding:utf-8 -*-
from tkinter import *
from datetime import datetime
import RPi.GPIO as GPIO
from time import sleep

human_pin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(human_pin, GPIO.IN)

root = Tk()
# メインウィンドウサイズ
root.geometry('720x480')
# メインウィンドウタイトル
root.title('PiDisplay')

# Canvas 作成
c = Canvas(root, bg='#FFFFFF', width=500, height=480)
c.pack(expand=True, fill='x', padx=5, side='left')

# 文字列作成
ch = c.create_text(350, 80, font=('', 60, 'bold'), fill='red')
cd = c.create_text(350, 180, font=('', 40, 'bold'), fill='black')
ct = c.create_text(350, 280, font=('', 80), fill='black')
cf = c.create_text(350, 400, font=('', 40), fill='blue')

# メインウィンドウの最大化
root.attributes("-zoomed", "1")
# 常に最前面に表示
root.attributes("-topmost", False)

def cupdate():

    hpin=GPIO.input(human_pin)
    if hpin == 1:
        h='人が来ました！' #'Human Detected'
    else:
        h='誰もいません' #'No Human'
    print(h)

    # 現在時刻を表示
    now = datetime.now()
    d = '{0:0>4d}年{1:0>2d}月{2:0>2d}日 ({3})'.format(now.year, now.month, now.day, now.strftime('%a'))
    t = '{0:0>2d}:{1:0>2d}:{2:0>2d}'.format(now.hour, now.minute, now.second)
    c.itemconfigure(ch, text='Pi Display')
    c.itemconfigure(cd, text=d)
    c.itemconfigure(ct, text=t)
    c.itemconfigure(cf, text=h)
    c.update()
    # 1秒間隔で繰り返す
    root.after(1000, cupdate)

# コールバック関数を登録
root.after(1000, cupdate)
# メインループ
root.mainloop()

GPIO.cleanup()
