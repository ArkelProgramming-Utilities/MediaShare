import os
import random
import string
import json
import subprocess
import datetime
import time

import wand.image
from flask import Response
from wand.image import Image as WImage
from io import BytesIO
import os.path
import cv2
import os
import numpy as np
from werkzeug.wsgi import FileWrapper

img_ = []
img_c = []
vid_ = []
vid_c = []
txt_ = []
exclude_ = []

ROOTDIR = ""
METAINFDIR = ""


def loadConfig():
    file = open("config/config.json", "r")
    data = json.loads(file.read())
    file.close()

    global img_
    global img_c
    global vid_
    global vid_c
    global txt_
    global exclude_
    global ROOTDIR
    global METAINFDIR

    ROOTDIR = data["rootdir"]
    METAINFDIR = data["metainf"]
    img_ = data["image"]
    vid_ = data["video"]
    txt_ = data["text"]
    exclude_ = data["exclude"]
    img_c = data["image_conv"]
    vid_c = data["video_conv"]


loadConfig()


def generateToken(num):
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num))
    return token


PREVIEW_IMG_SIZE = 96
PREVIEW_TEXT_SIZE = 64


def sendFile(file_, mod):
    if not file_:
        return json.dumps({
            "status_code": 2
        })

    file_ = os.path.join(ROOTDIR, file_)

    t = getType(file_)
    if t == "img" or t == "imgc":
        if t == "imgc":
            img = wand.image.Image(filename=file_)
            img = np.array(img)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if t == "img":
            img = cv2.imread(file_)

        if "p" in mod:
            wid = min(img.shape[0], img.shape[1])
            img = img[int((img.shape[0] - wid) / 2):int((img.shape[0] + wid) / 2),
                  int((img.shape[1] - wid) / 2):int((img.shape[1] + wid) / 2)]

            if img.shape[0] > PREVIEW_IMG_SIZE:
                img = cv2.resize(img, (PREVIEW_IMG_SIZE, int(PREVIEW_IMG_SIZE * img.shape[0] / img.shape[1])))

        is_success, im_buf_arr = cv2.imencode(".png", img)
        bytes_out = im_buf_arr.tobytes()

        b = BytesIO(bytes_out)
        w = FileWrapper(b)
        return Response(w, direct_passthrough=True)
    if t == "vid" or t == "vidc":
        if "t" in mod:  # thumbnail
            vcap = cv2.VideoCapture(file_)
            res, img = vcap.read()

            wid = min(img.shape[0], img.shape[1])
            img = img[int((img.shape[0] - wid) / 2):int((img.shape[0] + wid) / 2),
                  int((img.shape[1] - wid) / 2):int((img.shape[1] + wid) / 2)]

            if img.shape[0] > PREVIEW_IMG_SIZE:
                img = cv2.resize(img, (PREVIEW_IMG_SIZE, int(PREVIEW_IMG_SIZE * img.shape[0] / img.shape[1])))

            is_success, im_buf_arr = cv2.imencode(".png", img)
            bytes_out = im_buf_arr.tobytes()
            b = BytesIO(bytes_out)
            w = FileWrapper(b)
            return Response(w, direct_passthrough=True)
        else:
            file = open(file_, "rb")
            bytes_out = file.read()
            file.close()

            print("return image")
            b = BytesIO(bytes_out)
            w = FileWrapper(b)
            return Response(w, direct_passthrough=True)
    elif t == "txt":
        file = open(file_, "r")
        w = file.read()
        if "p" in mod:
            w = w[:min(len(w), PREVIEW_TEXT_SIZE)]
        file.close()

        return w
    else:
        return json.dumps({
            "error_code": 2
        })


def getType(filename):
    filename1, filetype1 = os.path.splitext(filename)
    filetype = filetype1[1:].lower()

    if os.path.isdir(filename):
        return "dir"
    elif filetype in img_:
        return "img"
    elif filetype in img_c:
        return "imgc"
    elif filetype in vid_:
        return "vid"
    elif filetype in vid_c:
        return "vidc"
    elif filetype in txt_:
        return "txt"
    elif filetype in exclude_:
        return "exc"
    else:
        return "unk"


def getDirInfo(parent):
    info = []
    dates = []
    if ".." in parent:  # no backtracking
        return []

    lst = os.listdir(os.path.join(ROOTDIR, parent))

    for elem in (os.path.join(ROOTDIR, parent, x) for x in lst):

        if os.path.isdir(elem):
            info.append((os.path.basename(elem), "dir"))
            dates.append(0)
        else:
            filename_, filetype = os.path.splitext(elem)
            filetype = filetype[1:].lower()
            filename = elem[len(ROOTDIR) + 1:]

            if filetype in exclude_:
                continue

            cfgfile = os.path.join(METAINFDIR, os.path.basename(elem) + ".json")
            if os.path.exists(cfgfile):
                with open(cfgfile, "r") as obj:
                    data = json.loads(obj.read())
                    obj.close()

                timestamp = data["photoTakenTime"]["timestamp"]
                dates.append(int(timestamp))
            else:
                dates.append(0)

            info.append((filename, getType(filename), filetype))

    info_ = [x for _, x in sorted(zip(dates, info))]
    if len(info_) != 0:
        return info_
    return info
