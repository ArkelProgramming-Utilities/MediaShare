import json
import subprocess
import os.path as path
import os
import datetime
import multiprocessing as mp


def parseDate(str):
    try:
        return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
    except:
        return None


def getFileMetadata(filein):
    process = subprocess.Popen(["hachoir-metadata", filein], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               universal_newlines=True)
    NAME = ".".join(path.basename(filein).split(".")[:2])

    for output in process.stdout:
        # print(output)
        val = output[output.index(":") + 1:].strip()
        if "Date-time digitized" in output:
            PTT = parseDate(val)
        if "Creation date" in output:
            CTT = parseDate(val)
        if "Latitude" in output:
            LAT = float(val)
        if "Longitude" in output:
            LONG = float(val)
        if "Altitude" in output:
            ALT = float(val[:-len(" meters")])

    try:
        data = json.dumps({
            "title": NAME,
            "description": "",
            "creationTime": {
                "timestamp": CTT.timestamp(),
                "formatted": "Jul 22, 2019, 10:48:15 AM UTC"
            },
            "photoTakenTime": {
                "timestamp": PTT.timestamp(),
                "formatted": PTT.strftime("%b %d, %Y, %I:%M:%S %p UTC")
            },
            "geoData": {
                "latitude": LAT,
                "longitude": LONG,
                "altitude": ALT,
                "latitudeSpan": 0.0,
                "longitudeSpan": 0.0
            },
            "geoDataExif": {
                "latitude": "n/a",
                "longitude": "n/a",
                "altitude": "n/a",
                "latitudeSpan": 0.0,
                "longitudeSpan": 0.0
            },
            "googlePhotosOrigin": {
                "mobileUpload": {
                    "deviceType": "localconv"
                }
            }
        })
    except:
        return None
    return data


def getFiles(dir):
    files_ = []

    for entry in os.listdir(dir):
        e = path.join(dir, entry)
        if path.isfile(e):
            files_.append(e)
        elif path.isdir(e):
            files_.extend(getFiles(e))

    return files_


i = 0
count = 0

def func_(file):
    global i
    i += 1
    exists = "exists"
    p = path.join("C:\\Users\\nicho_\\Documents\\meta", path.basename(file) + ".json")
    # print(p)
    if not path.exists(p):
        data = getFileMetadata(file)
        if data:
            f = open(p, "w")
            f.write(data)
            f.close()
            exists = "worked"
        else:
            exists = "broke"
    print(str(i) + "/" + str(count) + " -" + exists)


if __name__ == "__main__":
    files = getFiles("F:\\Media")
    count = len(files)

    pool = mp.Pool(mp.cpu_count())
    result = pool.map(func_, files)
