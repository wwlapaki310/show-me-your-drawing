from PIL import Image, ImageDraw
import cv2
import numpy as np
from io import BytesIO

images = []
for i in range(6):
    img=Image.open('img/image'+str(i)+'.png')
    img=np.asarray(img)
    #img=cv2.imread('img/image'+str(i)+'.png')
    img_prop = []
    for x in img:
        tmp = []
        for y in x:
            tmp.append(255 - y[3]) # Aの値を抽出して白黒反転
        img_prop.append(tmp)
    img_prop = np.array(img_prop).astype("uint8")
    pilImg = Image.fromarray(np.uint8(img_prop))

    images.append(pilImg)

images[0].save('img/drawing.gif',save_all=True, append_images=images[1:], duration=40, loop=0)