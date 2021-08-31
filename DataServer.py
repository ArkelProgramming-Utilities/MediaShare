import os
import base64
import random
import string

img_ = ["jpg", "png", "bmp", "heic"]
vid_ = ["mov", "mp4", "mkv"]
txt_ = ["txt", "json", "xml", "cfg", "dat"]
exclude_ = ["lnk", "desktop", "exe", "ini"]
ROOTDIR = "datain"
#ROOTDIR = "F:\\Games"

def generateToken(num):
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num))
    return token


def getType(filename):
    filename1, filetype1 = os.path.splitext(filename)
    filetype = filetype1[1:].lower()

    if os.path.isdir(filename):
        return "dir"
    elif filetype in img_:
        return "img"
    elif filetype in vid_:
        return "vid"
    elif filetype in txt_:
        return "txt"
    else:
        return "unk"


mpp = 9  # media per page


def getDirInfo(parent, page):
    info = []
    if ".." in parent:  # no backtracking
        return []

    lst = os.listdir(os.path.join(ROOTDIR, parent))

    if page * mpp >= len(lst):
        return []
    #lst = lst[page * mpp:min((page + 1) * mpp, len(lst))]  # select specific parts

    for elem in (os.path.join(ROOTDIR, parent, x) for x in lst):

        if os.path.isdir(elem):
            info.append((os.path.basename(elem), "dir"))
        else:
            filename_, filetype = os.path.splitext(elem)
            filetype = filetype[1:].lower()
            filename = elem[len(ROOTDIR)+1:]

            if filetype in exclude_:
                continue

            if filetype in img_:
                info.append((filename, "img", filetype))
            elif filetype in vid_:
                info.append((filename, "vid", filetype))
            elif filetype in txt_:
                info.append((filename, "txt", filetype))
            else:
                info.append((filename, "unk", filetype))
    return info
