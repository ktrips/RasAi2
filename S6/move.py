# -*- coding: utf-8 -*-
from gpiozero import Motor
#from time import sleep
# タイマーのライブラリ
import time
# 引数取得
import sys

# GPIO端子の設定
motor = Motor(forward=20, backward=21)

# 引数
param = sys.argv

# 第1引数
# go : 回転
# back : 逆回転
# break : ブレーキ
order = param[1]

# 第2引数 秒数
second = int(param[2])

if order == "forward":
    if second == 0:
        print("回転 止めるときはbreak 0コマンド！")
    else:
        print(str(second)+"s Forward")
    motor.forward(0.5)
    time.sleep(second)
    motor.stop()

elif order == "back":
    if second == 0:
        print("逆回転 止めるときはbreak 0コマンド！")
    else:
        print(str(second)+"s Backward")    
    motor.backward(0.5)
    time.sleep(second)
    motor.stop()

# 第2引数が0の場合は、ブレーキをしない
# 第1引数がbreakの場合は、ブレーキ
if order == "stop" or second != 0:
    print("Stop!")
    motor.stop()

