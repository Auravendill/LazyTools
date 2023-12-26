#!/bin/bash

mkdir exe
mkdir img
mkdir pdf
mkdir vid
mkdir gif

find . -type f -name "*.exe" -print0 | xargs -0 mv -t ./exe

find . -type f -name "*.png" -print0 | xargs -0 mv -t ./img
find . -type f -name "*.jpg" -print0 | xargs -0 mv -t ./img
find . -type f -name "*.heic" -print0 | xargs -0 mv -t ./img

find . -type f -name "*.pdf" -print0 | xargs -0 mv -t ./pdf

find . -type f -name "*.m4v" -print0 | xargs -0 mv -t ./vid
find . -type f -name "*.mp4" -print0 | xargs -0 mv -t ./vid
find . -type f -name "*.mov" -print0 | xargs -0 mv -t ./vid
find . -type f -name "*.mkv" -print0 | xargs -0 mv -t ./vid
find . -type f -name "*.avi" -print0 | xargs -0 mv -t ./vid
find . -type f -name "*.wmv" -print0 | xargs -0 mv -t ./vid
find . -type f -name "*.ts"  -print0 | xargs -0 mv -t ./vid
find . -type f -name "*.webm" -print0 | xargs -0 mv -t ./vid

find . -type f -name "*.gif" -print0 | xargs -0 mv -t ./gif

find . -type d -empty -delete -print
