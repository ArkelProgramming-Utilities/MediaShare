import json
import random
import subprocess
import os.path as path
import os
import datetime
import multiprocessing as mp
import timezonefinder, pytz
tf = timezonefinder.TimezoneFinder()


def parseDate(str):
    try:
        return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S").timestamp()
    except:
        return 0

def turnToUTC(dt, lat, long):
    #print("dt=" + str(dt))
    zone = tf.certain_timezone_at(lat=lat, lng=-long)
    local_time = pytz.timezone(zone)
    t1 = local_time.localize(datetime.datetime.fromtimestamp(dt))
    t2 = t1.astimezone(pytz.utc)

    if t2.timestamp() < 0:
        return 0
    return t2.timestamp()

def getFileMetadata(filein):
    process = subprocess.Popen(["hachoir-metadata", filein], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               universal_newlines=True)
    NAME = ".".join(path.basename(filein).split(".")[:2])

    PTT = 0
    CTT = 0
    LAT = 0
    LONG = 0
    ALT = 0

    didsomething = False

    log = []
    for output in process.stdout:
        # print(output)

        if ":" not in output:
            continue
        #print("output=" + output)
        val = output[output.index(":") + 1:].strip()
        key = output[:output.index(":")][2:]
        log.append(output + "   KEY=" + key + "|VAL=" +val)
        if "Unable to parse file" in output:
            break
        if key == "Date-time digitized":
            PTT = parseDate(val)
            didsomething = True
        if key == "Creation date":
            CTT = parseDate(val)
            didsomething = True
        if key == "Latitude":
            LAT = float(val)
            didsomething = True
        if key == "Longitude":
            LONG = float(val)
            didsomething = True
        if key == "Altitude":
            ALT = float(val[:-len(" meters")])
            didsomething = True

    if not didsomething:
        return None

    if not LAT or not LONG:
        return None

    if CTT ==0 and PTT == 0:
        print("------------------------------")
        for l in log:
            print(l)
        print("------------------------------")
        return None

    print("val=" + str(CTT) + ":" + str(PTT) + " lat=" + str(LAT) + " long=" + str(LONG))
    CTT = turnToUTC(CTT, LAT, LONG)
    PTT = turnToUTC(PTT, LAT, LONG)
    print("val2=" + str(CTT) + ":" + str(PTT))

    data = json.dumps({
        "title": NAME,
        "description": "",
        "creationTime": {
            "timestamp": CTT,
            "formatted": datetime.datetime.fromtimestamp(CTT).strftime("%b %d, %Y, %I:%M:%S %p UTC")
        },
        "photoTakenTime": {
            "timestamp": PTT,
            "formatted": datetime.datetime.fromtimestamp(PTT).strftime("%b %d, %Y, %I:%M:%S %p UTC")
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
    return data


def deleteBadMeta(file):
    try:
        f = open(file, "r")
        data = json.loads(f.read())
        f.close()

        if data["googlePhotosOrigin"]["mobileUpload"]["deviceType"] == "localconv":
            os.remove(file, True)
            print("removed")
    except:
        None


def getFiles(dir):
    files_ = []

    for entry in os.listdir(dir):
        e = path.join(dir, entry)
        if path.isfile(e):
            files_.append(e)
        elif path.isdir(e):
            files_.extend(getFiles(e))

    return files_


def func_2(file):
    deleteBadMeta(file)
    # print("found" + str(random.random()*3)[:2])


def func_(file):
    exists = "exists"
    p = path.join("F:\\meta\\artificial", path.basename(file) + ".json")
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
    print(exists)


if __name__ == "__main__":
    files = getFiles("F:\\Media")
    # files = os.listdir("F:\\meta")

    # files_ = []
    # for file in files:
    # files_.append(os.path.join("F:\\meta", file))

    #for file in files:
        #func_(file)
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(func_, files)
