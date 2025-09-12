#! /usr/bin/env python3

import cv2 as cv
from glob import glob
import os

if __name__ == "__main__":

    cameradata_dir = "../cameradata/livecamera1/test_data"
    output_dir = "./output"
    mask_dir = f"{output_dir}/mask"
    background_dir = f"{output_dir}/background"
    result_dir = f"{output_dir}/result"
    x_start, x_end = 10, 2262
    y_start, y_end = 10, 1000
    history = 200
    varThreshold = 50
    contour_area_max = 500

    os.makedirs(mask_dir, exist_ok=True)
    os.makedirs(result_dir, exist_ok=True)
    os.makedirs(background_dir, exist_ok=True)

    fnames = sorted(glob(f"{cameradata_dir}/09/*jpg")) + sorted(
        glob(f"{cameradata_dir}/10/*jpg")
    )
    print(f"img num: {len(fnames)}")

    backsub = cv.createBackgroundSubtractorMOG2(
        history=history, varThreshold=varThreshold  # , detectShadows=True
    )

    for i, fname in enumerate(fnames):
        print(fname)
        frame_all = cv.imread(fname)
        frame = frame_all[y_start:y_end, x_start:x_end]
        if frame is None:
            print("skip")
            continue

        #
        fgmask = backsub.apply(frame)
        background = backsub.getBackgroundImage()
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, None)

        contours, _ = cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # contours, _ = cv.findContours(fgmask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv.contourArea(c) < contour_area_max:
                continue
            x, y, w, h = cv.boundingRect(c)
            cv.rectangle(
                frame,
                (x_start + x, y_start + y),
                (x_start + x + w, y_start + y + h),
                (0, 255, 0),
                2,
            )
            # contour_shifted = c + [x_start, y_start]
            # cv.drawContours(frame_all, [contour_shifted], -1, (0, 255, 0), 2)

        if background is not None:
            cv.rectangle(frame_all, (x_start, y_start), (x_end, y_end), (0, 0, 255), 2)
            cv.imwrite(f"{result_dir}/result_{i:04d}.jpg", frame_all)
            cv.imwrite(f"{mask_dir}/mask_{i:04d}.jpg", fgmask)
            cv.imwrite(f"{background_dir}/background_{i:04d}.jpg", background)
