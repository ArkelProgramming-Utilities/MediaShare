import json
import os
import numpy as np
import whatimage
from wand.image import Image
from io import BytesIO
import os.path
import cv2
import flask
from flask import Flask, send_from_directory, Response
from werkzeug.wsgi import FileWrapper

from DataServer import getDirInfo, getType, ROOTDIR

app = Flask(__name__)

registry = ["index.html", "index.js", "folder.png", "favicon.ico"]


@app.route('/')
def index():
    # print("REQ=" + flask.request.user_agent.string.lower())
    if "mobile" in flask.request.user_agent.string.lower():
        return send_from_directory("static/", "index_m.html")
    return send_from_directory("static/", "index.html")


@app.route('/static/<file>')
def filefetch(file):
    if file in registry:
        return send_from_directory("static/", file)
    return None


@app.route('/media-info')
def dirinfo():
    page = int(flask.request.headers.get("page", 0))
    parent = flask.request.headers.get("dir", "")

    print(parent)
    data = getDirInfo(parent, page)
    return json.dumps(data)


@app.route("/get-media")
def getMedia():
    file_ = flask.request.headers.get("file", "null")
    size = int(flask.request.headers.get("size", -1))

    file = os.path.join(ROOTDIR, file_)

    type = getType(file)
    if type == "img":
        img = Image(filename=file)
        img.format = "png"
        img = np.array(img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if size != -1 and img.shape[0] > size:
            img = cv2.resize(img, (size, int(size * img.shape[0] / img.shape[1])))

        is_success, im_buf_arr = cv2.imencode(".png", img)
        print(is_success)
        bytes_out = im_buf_arr.tobytes()

        b = BytesIO(bytes_out)
        w = FileWrapper(b)
        return Response(w, mimetype="text/plain", direct_passthrough=True)

    elif type == "txt":
        file = open(file, "r")
        w = file.read()
        if size != -1:
            w = w[:min(len(w), size)]
        file.close()

        return w
    else:
        file = open(file, "rb")
        bytes_out = file.read()
        file.close()

        b = BytesIO(bytes_out)
        w = FileWrapper(b)
        return Response(w, mimetype="text/plain", direct_passthrough=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=25565)
