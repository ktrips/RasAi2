# -*- encoding:utf-8 -*-
import requests
import urllib
import json
from io import BytesIO
import math

imgFaceapi = 'face.jpg'
urlFaceapi = 'https://raspiface.cognitiveservices.azure.com/face/v1.0/detect'
keyFaceapi = 'xxx'
retFaceapi = 'age,gender,smile,emotion'

def useFaceapi(url, key, ret, image):
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

