import json
import os
from io import BytesIO
import os.path
import cv2
from PIL import Image
import flask
from flask import Flask, send_from_directory, Response
from werkzeug.wsgi import FileWrapper

from DataServer import getDirInfo, getType, ROOTDIR

app = Flask(__name__)

registry = ["index.html", "index.js", "folder.png"]


@app.route('/')
def index():
    # print("REQ=" + flask.request.user_agent.string.lower())
    if "mobile" in flask.request.user_agent.string.lower():
        print("PHONE")
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
    imgsize = int(flask.request.headers.get("size", "null"))

    file = os.path.join(ROOTDIR, file_)
    if getType(file) == "img":
        img = cv2.imread(file)

        if imgsize != -1 and img.shape[0] > imgsize:
            img = cv2.resize(img, (imgsize, int(imgsize * img.shape[0] / img.shape[1])))

        is_success, im_buf_arr = cv2.imencode(".jpg", img)
        print(is_success)
        bytes_out = im_buf_arr.tobytes()
    else:
        file = open(file, "rb")
        bytes_out = file.read()
        file.close()

    b = BytesIO(bytes_out)
    w = FileWrapper(b)

    return Response(w, mimetype="text/plain", direct_passthrough=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=25565)
