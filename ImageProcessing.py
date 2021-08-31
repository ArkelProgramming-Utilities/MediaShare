import os
import os.path as path

import cv2
import numpy as np
from wand.image import Image

from DataServer import ROOTDIR


def getDirFiles(dir_):
    files_ = []
    for entry_ in os.listdir(dir_):
        entry = path.join(dir_, entry_)
        if path.isfile(entry):
            files_.append(entry)
        elif path.isdir(entry):
            files_.extend(getDirFiles(entry))

    return files_

extens = ["png", "jpg", "heic", "gif", "bmp"]

files = getDirFiles(ROOTDIR)
for file in files:
    print(file)
    if os.path.splitext(file)[1][1:].lower() not in extens:
        continue


    img = Image(filename=file)
    img.format = "png"
    img = np.array(img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    minsize = min(img.shape[0], img.shape[1])
    img = img[int((img.shape[0]-minsize)/2):int((img.shape[0]+minsize)/2), int((img.shape[1]-minsize)/2):int((img.shape[1]+minsize)/2)] #crop to square

    img = cv2.resize(img, (256, 256))

    dat = img.reshape(256*256,)

    #print(dat)

    path_ = path.join("dataset", path.basename(file))
    #print(path_)
    cv2.imwrite(path_, img)

