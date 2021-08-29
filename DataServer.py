import os
import base64

img_ = ["jpg", "png", "bmp"]
vid_ = ["mov", "mp4", "mkv"]
exclude_ = ["lnk", "desktop", "exe", "ini"]
#ROOTDIR = "C:\\Users\\nicho\\Videos"
ROOTDIR = "F:\\"

def getType(filename):
    filename1, filetype1 = os.path.splitext(filename)
    filetype = filetype1[1:].lower()

    if os.path.isdir(filename):
        return "dir"
    elif filetype in img_:
        return "img"
    elif filetype in vid_:
        return "vid"
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
        filename = elem[len(ROOTDIR):]

        if os.path.isdir(elem):
            info.append((os.path.basename(elem), "dir"))
        else:
            filename_, filetype = os.path.splitext(elem)
            filetype = filetype[1:].lower()

            if filetype in exclude_:
                continue

            if filetype in img_:
                info.append((filename, "img"))
            elif filetype in vid_:
                info.append((filename, "vid", filetype))
            else:
                info.append((filename, "unk"))
    return info
