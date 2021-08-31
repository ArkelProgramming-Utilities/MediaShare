import json
import os
import numpy as np
import hashlib
from wand.image import Image
from io import BytesIO
import os.path
import cv2
import hmac
import flask
from flask import Flask, send_from_directory, Response
from werkzeug.wsgi import FileWrapper

from DataServer import getDirInfo, getType, ROOTDIR, generateToken

app = Flask(__name__)

registry = ["index.html", "index.js", "folder.png", "favicon.ico"]
token = None

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
    token_ = flask.request.cookies.get("auth_token")

    if token_ != token:
        return json.dumps({
            "status_code": 2
        })

    page = int(flask.request.headers.get("page", 0))
    parent = flask.request.headers.get("dir", "")

    data = getDirInfo(parent, page)
    return json.dumps(data)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    password = flask.request.form.get("password")
    hash_ = hashlib.sha1(password.encode())

    if hmac.compare_digest(savedhash, hash_.hexdigest()):
        global token
        token = generateToken(26)

        return json.dumps({
            "status_code": 0,
            "auth_token": token
        })

    return json.dumps({
        "status_code": 1
    })


@app.route("/get-media")
def getMedia():
    token_ = flask.request.cookies.get("auth_token")

    if token_ != token:
        return json.dumps({
            "status_code": 2
        })

    file_ = flask.request.headers.get("file", None)
    size = int(flask.request.headers.get("size", -1))

    if not file_:
        return json.dumps({
            "status_code": 2
        })

    file_ = os.path.join(ROOTDIR, file_)

    type = getType(file_)
    if type == "img":
        img = Image(filename=file_)
        img.format = "png"
        img = np.array(img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if size != -1 and img.shape[0] > size:
            img = cv2.resize(img, (size, int(size * img.shape[0] / img.shape[1])))

        is_success, im_buf_arr = cv2.imencode(".png", img)
        bytes_out = im_buf_arr.tobytes()

        b = BytesIO(bytes_out)
        w = FileWrapper(b)
        return Response(w, direct_passthrough=True)

    elif type == "txt":
        file = open(file_, "r")
        w = file.read()
        if size != -1:
            w = w[:min(len(w), size)]
        file.close()

        return w
    else:
        file = open(file_, "rb")
        bytes_out = file.read()
        file.close()

        b = BytesIO(bytes_out)
        w = FileWrapper(b)
        return Response(w, direct_passthrough=True)


if __name__ == '__main__':
    file = open("private.txt", "r")
    savedhash = file.read()
    file.close()
    app.run(host="192.168.1.157", port=25565, ssl_context=('certificate\\cert.pem', 'certificate\\key.pem'))
