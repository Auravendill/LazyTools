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

#Nothing for now here...

cd(path.expanduser("~"))
cl("cargo install topgrade cargo-update cargo-cache bottom tealdear")
