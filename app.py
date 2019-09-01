from flask import Flask
from flask import render_template
from flask import request
from PIL import Image
from PIL import ImageDraw, ImageFont
from collections import namedtuple
import math
from requests_oauthlib import OAuth1Session
import json
import base64
from pathlib import Path
from io import BytesIO
import numpy as np
import os

app = Flask(__name__)

count=0

@app.route('/', methods = ["GET" , "POST"])
def index():
    global count
    if request.method == 'POST':
        try:
            base64_png = request.form['img']
            code = base64.b64decode(base64_png.split(',')[1])  # remove header
            image_decoded = Image.open(BytesIO(code))
            image_decoded.save('static/img/image'+str(count)+'.png')
            count +=1
            return "img_capture"
        except:
            gousei=request.json["name"]
            os.remove('static/img/drawing.gif')
            images=[]
            print(gousei)
            for i in range(count):
                img=Image.open('static/img/image'+str(i)+'.png')
                img=np.asarray(img)
                img_prop = []
                for x in img:
                    tmp = []
                    for y in x:
                        tmp.append(255 - y[3])
                    img_prop.append(tmp)
                img_prop = np.array(img_prop).astype("uint8")
                pilImg = Image.fromarray(np.uint8(img_prop))
                images.append(pilImg)
                os.remove('static/img/image'+str(i)+'.png')
            images[0].save('static/img/drawing.gif',save_all=True, append_images=images[1:], duration=500, loop=0)
            count=0
            return render_template('result.html',message='Hello')
    else:
        return render_template('index.html',message='Hello')


@app.route('/result', methods = ["GET" , "POST"])
def result():
    return render_template("result.html")


if __name__ == "__main__":
    app.run()

    