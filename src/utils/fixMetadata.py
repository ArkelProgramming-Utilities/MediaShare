import json
import os.path as path
import os
import datetime
import multiprocessing as mp
import timezonefinder, pytz
tf = timezonefinder.TimezoneFinder()
from PIL import Image
import subprocess
import os


def parseDate(str):
    try:
        return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S").timestamp()
    except:
        return 0

def turnToUTC(dt):
    #print("dt=" + str(dt))
    #zone = tf.certain_timezone_at(lat=lat, lng=-long)
    local_time = pytz.timezone("US/Pacific")
    t1 = local_time.localize(datetime.datetime.fromtimestamp(dt))
    t2 = t1.astimezone(pytz.utc)

    if t2.timestamp() < 0:
        return 0
    return t2.timestamp()

def getFileMetadata(filein):
    process = subprocess.Popen(["hachoir-metadata", filein], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               universal_newlines=True)
    NAME = ".".join(filein.split("\\")[-1].split(".")[:-1])

    CDT = -1
    MDT = -1

    for output in process.stdout:
        #print(output)

        if ":" not in output:
            continue
        #print("output=" + output)
        val = output[output.index(":") + 1:].strip()
        key = output[:output.index(":")][2:]
        
        if "Unable to parse file" in output:
            break
        if key == "Creation date":
            CDT = parseDate(val)
        if key == "Last modification":
            MDT = parseDate(val)

    if CDT ==-1 and MDT==-1:
        return None

    FDT = min(CDT,MDT)
    try:
        data = json.dumps({
        "title": NAME,
        "description": "",
        "localtimezone":"PST",
        "creationTime": {
            "timestamp": int(FDT),
            "formatted": datetime.datetime.fromtimestamp(FDT).strftime("%b %d, %Y %H:%M:%S UTC")
        }
        })
    except:
        return None
    return data

def parseFileName(file):
    NAME = ".".join(file.split("\\")[-1].split(".")[:-1])
    timestamp = -1
    
    if timestamp==-1:
        try:
            #"ArmA 3 2021.11.25 - 18.07.09.04.DVR"
            date = NAME.split(" ")[-3:]
            datestr = "".join(date)[:-7]
            timestamp = turnToUTC(datetime.datetime.strptime(datestr, "%Y.%m.%d-%H.%M.%S").timestamp())
        except:
            None
    if timestamp==-1:
        try:
            #"Arma 3 5_7_2021 2_07_52 PM"
            date = NAME.split(" ")[-3:]
            datestr = "-".join(date)
            timestamp = turnToUTC(datetime.datetime.strptime(datestr, "%m_%d_%Y-%I_%M_%S-%p").timestamp())
        except:
            None
            
    if timestamp==-1:
        try:
            #"Tom Clancy_s The Division 2 2020.03.06 - 18.31."
            date = NAME.split(" ")[-3:]
            datestr = "".join(date)[:-1]
            timestamp = turnToUTC(datetime.datetime.strptime(datestr, "%Y.%m.%d-%H.%M").timestamp())
        except:
            None
    
    if timestamp==-1:
        try:
            #"Space Engineers Screenshot 2019.06.07 - 19.45.0"
            date = NAME.split(" ")[-3:]
            datestr = "".join(date)
            timestamp = turnToUTC(datetime.datetime.strptime(datestr, "%Y.%m.%d-%H.%M.%S").timestamp())
        except:
            None
    
    if timestamp==-1:
        try:
            #"Space Engineers Screenshot 2019.06.07 - 19.45.0.52"
            date = NAME.split(" ")[-3:]
            datestr = "".join(date)[:-3]
            timestamp = turnToUTC(datetime.datetime.strptime(datestr, "%Y.%m.%d-%H.%M.%S").timestamp())
        except:
            None
    
    if timestamp==-1:
        try:
            #"Replay 2020-02-16 17-45-54"
            date = NAME.split(" ")[-2:]
            datestr = "-".join(date)
            timestamp = turnToUTC(datetime.datetime.strptime(datestr, "%Y-%m-%d-%H-%M-%S").timestamp())
        except:
            None
    
    if timestamp==-1:
        return None
    
    data = json.dumps({
    "title": NAME,
    "description": "",
    "localtimezone":"PST",
    "creationTime": {
        "timestamp": int(timestamp),
        "formatted": datetime.datetime.fromtimestamp(timestamp).strftime("%b %d, %Y %H:%M:%S UTC")
    }
    })
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

    # print("found" + str(random.random()*3)[:2])


def func_(file):
    exists = "exists"
    p = path.join("E:\\meta3", path.basename(file) + ".json")
    # print(p)
    if not path.exists(p):
        data = getFileMetadata(file)
        if data:
            f = open(p, "w")
            f.write(data)
            f.close()
            exists = "worked"
        else:
            data1 = parseFileName(file)
            if data1:
                f = open(p, "w")
                f.write(data1)
                f.close()
                exists = "worked"
            else:
                exists = "broke"
                data2 = json.dumps({
                    "title": ".".join(file.split("\\")[-1].split(".")[:-1]),
                    "description": "",
                    "localtimezone":"PST",
                    "creationTime": {
                        "timestamp": -1,
                        "formatted": ""
                    }
                    })
                f = open(p, "w")
                f.write(data2)
                f.close()
    print(exists)

def rename_(item):
    id = item[0]+1000
    file = item[1]
    
    p = path.join("E:\\meta1", path.basename(file) + ".json")
    p1 = path.join("E:\\meta1", str(id) + ".json")
    
    f = os.path.join("\\".join(os.path.splitext(file)[0].split("\\")[:-1]), str(id) + "." + file.split(".")[-1])
    os.rename(file, f)
    os.rename(p, p1)
    

if __name__ == "__main__":
    files = getFiles("E:\\Games")
    dat = [[x, i] for x, i in enumerate(files)]

    #parseFileName("")
    #print(getFileMetadata(files))
    # files = os.listdir("F:\\meta")

    # files_ = []
    # for file in files:
    # files_.append(os.path.join("F:\\meta", file))

    #for file in files:
        #func_(file)
        
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(rename_, dat)
    #result = pool.map(func_, files)
