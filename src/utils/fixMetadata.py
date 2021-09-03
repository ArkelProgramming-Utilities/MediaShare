def getFileDate(file):
    process = subprocess.Popen(["hachoir-metadata", file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               universal_newlines=True)
    for output in process.stdout:
        # print(output)
        if "Date-time digitized" in output:
            dt = datetime.datetime.strptime(output[output.index(":") + 1:].strip(), "%Y-%m-%d %H:%M:%S")
            return dt
    return datetime.datetime.fromtimestamp(0)