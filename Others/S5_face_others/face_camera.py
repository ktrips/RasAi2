# -*- encoding:utf-8 -*-
import requests
import urllib
import json
from io import BytesIO
from PIL import Image, ImageDraw
import math
import os

# Bing Face API 用設定
# ------------------------------
os.system("raspistill -o face2.jpg")
imgFaceapi = 'face2.jpg'
#urlFaceapi = 'https://raspiface.cognitiveservices.azure.com/'

#urlFaceapi = 'https://api.projectoxford.ai/face/v1.0/detect'
urlFaceapi = 'https://raspiface.cognitiveservices.azure.com/face/v1.0/detect'

keyFaceapi = '468517bcf79942d9aad4660060b426d1'
retFaceapi = 'age,gender,smile,emotion'
#headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'

# ----------------------------------------------------------------------
# ■画像分析（Bing Face API） for python 3.x
# ----------------------------------------------------------------------
def useFaceapi(url, key, ret, image):

    # サーバ問合せ
    # ------------------------------
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


# ----------------------------------------------------------------------
# ■分析実行
# ----------------------------------------------------------------------

# Bing Face API を使う
# ------------------------------
resFaceapi = useFaceapi(urlFaceapi, keyFaceapi, retFaceapi, imgFaceapi)
print(resFaceapi)

for face in resFaceapi:
  left  = face["faceRectangle"]["left"]
  top   = face["faceRectangle"]["top"]
  right = face["faceRectangle"]["left"]+face["faceRectangle"]["width"]
  bottom= face["faceRectangle"]["top"]+face["faceRectangle"]["height"]
  age   = math.floor(face["faceAttributes"]["age"])
  gender= face["faceAttributes"]["gender"]
  print(left, top, right, bottom, age, gender)

data = open(imgFaceapi, 'rb').read()
img = Image.open(BytesIO(data)) #response.content))
draw = ImageDraw.Draw(img)
#for face in detected_faces:
draw.rectangle(((left,top),(right,bottom)), outline='red')
draw.text((left,bottom+5), str(age)+","+gender, fill=(255,0,0))
img.show()

