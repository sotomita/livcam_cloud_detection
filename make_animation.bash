#! /bin/bash

ffmpeg -framerate 10 -i output/background/background_%04d.jpg -c:v libx264 -pix_fmt yuv420p ./output/background.mp4
ffmpeg -framerate 10 -i output/result/result_%04d.jpg -c:v libx264 -pix_fmt yuv420p ./output/result.mp4