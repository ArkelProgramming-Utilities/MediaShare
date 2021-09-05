import json
import hashlib
import hmac
import socket
import flask
from flask import Flask, send_from_directory
from DataServer import getDirInfo, generateToken, sendFile

app = Flask(__name__)

registry = ["index.html", "index.js", "folder.png", "favicon.ico"]
token = None


@app.route('/')
def index():
    #if "mobile" in flask.request.user_agent.string.lower():
        #return send_from_directory("../static/", "index_m.html")
    return send_from_directory("../static/", "index.html")


@app.route('/static/<file>')
def filefetch(file):
    if file in registry:
        return send_from_directory("../static/", file)
    return None


@app.route('/media-info')
def dirinfo():
    token_ = flask.request.cookies.get("auth_token")

    if token_ != token:
        return json.dumps({
            "status_code": 2
        })

    parent = flask.request.headers.get("dir", "")

    data = getDirInfo(parent)
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
    modifiers = flask.request.headers.get("mod", [])

    return sendFile(file_, list(modifiers))


if __name__ == '__main__':
    # read config
    file = open("config/private.txt", "r")
    savedhash = file.read()
    file.close()

    h_name = socket.gethostname()
    ip = socket.gethostbyname(h_name)
    app.run(host=ip, port=25565, ssl_context=('config\\cert.pem', 'config\\key.pem'))
