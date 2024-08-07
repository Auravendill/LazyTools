#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import random
import string

from numpy import rint

whitelist = ["mp4", "mp3", "webm", "png", "svg", "m4v", "gif", "bmp", "jpg", "pdf","rm","3gp",
             "mov", "mkv", "avi", "flv", "wmv", "mpg", "ts", "wav", "m4a", "webp",
             "heic", "exe", "mod","py","sh","obj","stl","skp","nds","n64","gba","ttf","step"]
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
    #elif(info=="application/vnd.microsoft.portable-executable"):
    #    suggested_ending = "exe"
    elif(info=="application/vnd.debian.binary-package"):
        suggested_ending = "deb"
    elif(info=="application/x-nintendo-ds-rom"):
        suggested_ending = "nds"
    elif(info=="application/x-n64-rom"):
        suggested_ending = "n64"
    elif(info=="application/x-gba-rom"):
        suggested_ending = "gba"
    elif(info=="application/vnd.sketchup.skp"):
        suggested_ending = "skp"
    elif(info=="font/sfnt"):
        suggested_ending = "ttf"
    elif(info=="application/x-iso9660-image"):
        suggested_ending = "iso"
    else:
        suggested_ending = info.split("/")[-1].split("-")[-1].strip().lower()
    if suggested_ending == "empty":
        print("Remove: "+filepath)
        os.remove(filepath)
    elif suggested_ending == "stream":
        return
    elif suggested_ending == "symlink":
        return
    elif suggested_ending == "dosexec":
        print("Warning: This is an exe file: "+filepath)
        suggested_ending = "exe"
    elif suggested_ending == "shellscript":
        suggested_ending = "sh"
    elif suggested_ending == "script.python":
        suggested_ending = "py"
    elif suggested_ending == "jpeg":
        suggested_ending = "jpg"
    elif suggested_ending == "3gpp":
        suggested_ending = "3gp"
    elif suggested_ending == "quicktime":
        suggested_ending = "mov"
    elif suggested_ending == "realmedia":
        suggested_ending = "rm"
    elif suggested_ending == "matroska":
        suggested_ending = "mkv"
    elif suggested_ending == "msvideo":
        suggested_ending = "avi"
    elif suggested_ending == "asf":
        suggested_ending = "wmv"
    elif suggested_ending == "mpeg":
        suggested_ending = "mpg"
    elif suggested_ending == "mp2t":
        suggested_ending = "ts"
    elif suggested_ending == "plain":
        suggested_ending = "txt"
    elif suggested_ending == "svg+xml":
        suggested_ending = "svg"
        # if not fast_option:
        return
    
    dirty_endings=["obj","stl","step","3mf","gcode","bat"]
    if ending.lower() in dirty_endings:
        suggested_ending=ending.lower()

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
