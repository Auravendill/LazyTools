#!/usr/bin/env python3

from os import chdir as cd
from os import path
from os import mkdir
from os import system as cl

print("Starting program...")

cd(path.expanduser("~"))

if not path.exists("Git"):
    print("Git folder missing. Generate new one")
    mkdir("Git")
cd("Git")

if not path.exists("Themes"):
    print("Themes folder missing. Generate new one")
    mkdir("Themes")
cd("Themes")

print("#"*10+"Orchis"+"#"*10)

if not path.exists("Orchis-theme"):
    print("Orchis-theme folder missing. Generate new one")
    cl("git clone https://github.com/vinceliuice/Orchis-theme.git")
cd("Orchis-theme")
cl("sudo ./install.sh --tweaks primary solid")

cd ("..")

if not path.exists("Orchis-kde"):
    print("Orchis-kde folder missing. Generate new one")
    cl("git clone https://github.com/vinceliuice/Orchis-kde.git")
cd("Orchis-kde")
cl("./install.sh --tweaks primary solid")

cd("..")

print("#"*10+"Cursor"+"#"*10)

if not path.exists("Vimix-cursors"):
    print("Vimix-cursors folder missing. Generate new one")
    cl("git clone https://github.com/vinceliuice/Vimix-cursors.git")
cd("Vimix-cursors")
cl("sudo ./install.sh")

cd("..")

print("#"*10+"Icons"+"#"*10)

if not path.exists("Reversal-icon-theme"):
    print("Reversal-icon-theme folder missing. Generate new one")
    cl("git clone https://github.com/yeyushengfan258/Reversal-icon-theme.git")
cd("Reversal-icon-theme")
cl("sudo ./install.sh -a")