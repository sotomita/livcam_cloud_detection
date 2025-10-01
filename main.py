#! /usr/bin/env python3

import cv2 as cv
from glob import glob
import os

import config


def get_fname_list(dir_list: list, ext: str = "jpg") -> list:
    fname_list = []
    for cameradata_dir in dir_list:
        fname_list += glob(f"{cameradata_dir}/*{ext}")
    fname_list.sort()
    return fname_list


def main():
    os.makedirs(config.mask_dir, exist_ok=True)
    os.makedirs(config.result_dir, exist_ok=True)
    os.makedirs(config.background_dir, exist_ok=True)

    fname_list = get_fname_list(config.cameradata_dir_list, ext="jpg")
    print(f"img num: {len(fname_list)}")

    backsub = cv.createBackgroundSubtractorMOG2(
        history=config.history, varThreshold=config.varThreshold
    )

    for i, fpath in enumerate(fname_list):
        print(fpath)
        frame_wide = cv.imread(fpath)
        frame = frame_wide[config.y_start : config.y_end, config.x_start : config.x_end]

        fgmask = backsub.apply(frame)
        background = backsub.getBackgroundImage()
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, None)

        contours, _ = cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for c in contours:
            if cv.contourArea(c) > config.contour_area_max:

                x, y, w, h = cv.boundingRect(c)
                cv.rectangle(
                    frame,
                    (config.x_start + x, config.y_start + y),
                    (config.x_start + x + w, config.y_start + y + h),
                    (0, 255, 0),
                    2,
                )

        if background is not None:
            cv.rectangle(
                frame_wide,
                (config.x_start, config.y_start),
                (config.x_end, config.y_end),
                (0, 0, 255),
                2,
            )
            cv.imwrite(f"{config.result_dir}/result_{i:04d}.jpg", frame_wide)
            cv.imwrite(f"{config.mask_dir}/mask_{i:04d}.jpg", fgmask)
            cv.imwrite(f"{config.background_dir}/background_{i:04d}.jpg", background)


if __name__ == "__main__":
    main()
