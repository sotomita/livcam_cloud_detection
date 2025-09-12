#! /bin/bash

ffmpeg -framerate 10 -i output/result/result_%04d.jpg -c:v libx264 -pix_fmt yuv420p result.mp4