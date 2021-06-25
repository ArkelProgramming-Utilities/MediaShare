import json

import flask
from flask import Flask, send_from_directory
from DataServer import getFilePaths, updateDictionary, getMediaPath, getMediaInfo

app = Flask(__name__)

dirs = ["C:\\Users\\nicho_\\Videos"]

@app.route('/')
def index():
    return send_from_directory("static/", "index.html")

@app.route('/media-info/<int:page>')
def mediainfo(page):
    data = getMediaInfo(page)
    return json.dumps(data)

@app.route("/get-media/<int:media_id>")
def getMedia(media_id):
    success, path = getMediaPath(media_id)
    if media_id == 0:
        print(path)

    if success:
        return flask.send_file(path)
    return

if __name__ == '__main__':
    for dir in dirs:
        files = getFilePaths(dir, True)
        updateDictionary(files)

    app.run()
