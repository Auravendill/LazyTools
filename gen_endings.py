import os
import sys
import subprocess
import shutil
import random
import string

from numpy import rint

whitelist = ["mp4", "mp3", "webm", "png", "svg", "m4v", "gif", "bmp", "jpg", "pdf","rm","3gp",
             "mov", "mkv", "avi", "flv", "wmv", "mpg", "ts", "wav", "m4a", "webp",
             "heic", "exe", "zip", "mod"]
collection = []
fast_option = False
directories = ["."]


def scan_folder(folder):
    f = [f.path for f in os.scandir(folder) if f.is_dir()]
    if f:
        for entry in f:
            scan_folder(entry)
    f = [f.path for f in os.scandir(folder) if f.is_file()]
    if f:
        for entry in f:
            if entry.endswith(".txt") or entry.endswith(".csv") or entry.endswith(".part"):
                continue
            operate_on_file(entry)


def operate_on_file(filepath):
    file = filepath.split("/")[-1]
    subdir = os.path.dirname(filepath)
    if file == "info.txt":
        return
    ending = file.split(".")[-1].strip()
    if ending == "part":
        return

    temp = subprocess.run(
        ['file', '--mime-type', '-b', filepath], stdout=subprocess.PIPE)
    info = temp.stdout.decode('utf-8').strip()

    #print(info)

    if(info=="audio/mpeg"):
        suggested_ending = "mp3"
    else:
        suggested_ending = info.split("/")[-1].split("-")[-1].strip().lower()
    if suggested_ending == "empty":
        print("Remove: "+filepath)
        os.remove(filepath)
    if suggested_ending == "stream":
        return
    if suggested_ending == "symlink":
        return
    if suggested_ending == "dosexec":
        print("Warning: This is an exe file: "+filepath)
        suggested_ending = "exe"
    if suggested_ending == "shellscript":
        suggested_ending = "sh"
    if suggested_ending == "jpeg":
        suggested_ending = "jpg"
    if suggested_ending == "3gpp":
        suggested_ending = "3gp"
    if suggested_ending == "quicktime":
        suggested_ending = "mov"
    if suggested_ending == "realmedia":
        suggested_ending = "rm"
    if suggested_ending == "matroska":
        suggested_ending = "mkv"
    if suggested_ending == "msvideo":
        suggested_ending = "avi"
    if suggested_ending == "asf":
        suggested_ending = "wmv"
    if suggested_ending == "mpeg":
        suggested_ending = "mpg"
    if suggested_ending == "mp2t":
        suggested_ending = "ts"
    if suggested_ending == "plain":
        suggested_ending = "txt"
    if suggested_ending == "svg+xml":
        suggested_ending = "svg"
        # if not fast_option:
        return
    if(ending != suggested_ending):
        if suggested_ending in whitelist:
            print(filepath)
            new_filepath = os.path.join(subdir, file.split(".")[
                                        0]+"."+suggested_ending)
            while (os.path.exists(new_filepath)):
                new_filepath = os.path.join(subdir, file.split(
                    ".")[0]+random.choice(string.ascii_letters)+"."+suggested_ending)
            print("Gets replaced with:\t" + new_filepath)
            shutil.move(filepath, new_filepath)
            return
        else:
            print(suggested_ending+"\t["+info+"]")
            print(filepath)

            if not suggested_ending in collection:
                collection.append(suggested_ending)


for directory in directories:
    scan_folder(directory)

if not len(collection)>0:
    exit()

collection.sort()
print("These endings were suggested, but ignored:")
for entry in collection:
    print(entry)
