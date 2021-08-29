import json
from io import BytesIO

import cv2
from PIL import Image
import flask
from flask import Flask, send_from_directory, Response
from werkzeug.wsgi import FileWrapper

from DataServer import getFilePaths, updateDictionary, getMediaPath, getMediaInfo, getType

app = Flask(__name__)

registry = ["index.html", "index.js"]

dirs = ["C:\\Users\\nicho\\Videos"]

@app.route('/')
def index():
    #print("REQ=" + flask.request.user_agent.string.lower())
    if "mobile" in flask.request.user_agent.string.lower():
        print("PHONE")
        return send_from_directory("static/", "index_m.html")
    return send_from_directory("static/", "index.html")

@app.route('/static/<file>')
def filefetch(file):
    if file in registry:
        return send_from_directory("static/", file)
    return None

@app.route('/media-info/<int:page>')
def mediainfo(page):
    data = getMediaInfo(page)
    return json.dumps(data)

@app.route("/get-media/<int:media_id>")
def getMedia(media_id):
    if "size" in flask.request.args:
        imgsize = int(flask.request.args.get("size"))
    else:
        imgsize = -1
    success, path = getMediaPath(media_id)
    if media_id == 0:
        print(path)

    if success:
        if getType(path) == "img":
            img = cv2.imread(path)

            if imgsize != -1 and img.shape[0]>imgsize:
                img = cv2.resize(img, (imgsize, int(imgsize * img.shape[0]/img.shape[1])))

            is_success, im_buf_arr = cv2.imencode(".jpg", img)
            print(is_success)
            bytes_out = im_buf_arr.tobytes()
        else:
            file = open(path, "rb")
            bytes_out = file.read()
            file.close()

        b = BytesIO(bytes_out)


        w = FileWrapper(b)
        return Response(w, mimetype="text/plain", direct_passthrough=True)
        #return flask.send_file(path)
    return

if __name__ == '__main__':
    for dir in dirs:
        files = getFilePaths(dir, True)
        updateDictionary(files)

    app.run(host="0.0.0.0", port=25565)
