import os
import base64
media = dict()

img_ = ["jpg", "png", "bmp"]
vid_ = ["mov", "mp4", "mkv"]
exclude_ = ["lnk", "desktop", "exe", "ini"]

def getMediaPath(id):
    if id not in media:
        return False, ""
    return True, media[id]

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

mediaperpage = 9
def getMediaInfo(page):
    info = []
    if page*mediaperpage >= len(media):
        return []
    for i in list(media.keys())[mediaperpage*page:min(mediaperpage*(1+page), len(media)-1)]:
        filename1, filetype1 = os.path.splitext(media[i])
        filename = os.path.basename(filename1)
        filetype = filetype1[1:].lower()

        if os.path.isdir(filename):
            info.append((i, filename, "dir"))
        elif filetype in img_:
            info.append((i, filename, "img"))
        elif filetype in vid_:
            info.append((i, filename, "vid", filetype))
        else:
            info.append((i, filename, "unk"))
    return info

def updateDictionary(files):
    index = len(media)
    for i, item in enumerate(files):
        media[index + i] = item
        print("[{0}]: {1}".format(index+i, item))


def getFilePaths(parentdir, recursive):
    directory = os.listdir(parentdir)
    files = []
    dirs = []
    for entry in directory:
        entry1 = os.path.join(parentdir, entry)
        if os.path.isfile(entry1):
            fn, fe = os.path.splitext(entry1)
            if fe[1:].lower() not in exclude_:
                files.append(entry1)
        elif os.path.isdir(entry1):
            dirs.append(entry1)

    if recursive:
        for dir2 in dirs:
            for files1 in getFilePaths(dir2, True):
                files.append(files1)

    return files
