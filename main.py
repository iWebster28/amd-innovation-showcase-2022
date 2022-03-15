import os
import glob

from PIL import Image, ImageGrab
import numpy as np
from time import sleep, time

import constants as cnst
# cnst.init()

OUTPUT_DIR = "output"
IMG_ERROR_THRESHOLD = 1500 # maybe just use opencv contour tracing instead? if contours change enough, take more images?
url = "https://www.youtube.com/watch?v=MBAJP-3ebDA" 

url="https://www.youtube.com/watch?v=HLzv8TVMQHo"

def main():
    remove_all_in_dir(OUTPUT_DIR)
    proof_of_concept()
    return

def remove_all_in_dir(dir):
    """Removes all files in directory `dir`

    Args:
        dir (str): directory to remove all files in
    """
    for file in glob.glob(os.path.join(dir, "*")):
        os.remove(file)
    return

def proof_of_concept():

    prev_screencap = None

    while True:
        screencap = ImageGrab.grab(bbox=None)
        if screencap is not None and prev_screencap is not None:
            # diff = ImageChops.difference(screencap, prev_screencap)
            # if diff.getbbox() is not None:
            #     print("DIFF")
            #     print(diff.getbbox())
            error = mean_squared_error(np.array(screencap), np.array(prev_screencap))
            print(error)
            if error > IMG_ERROR_THRESHOLD:
                print("DETETED FRAME CHANGE. SNAPPING.")
                image = screencap.save(os.path.join(OUTPUT_DIR, f"{str(int(time()))}.png"))


        prev_screencap = screencap
        # screencap.show()
        sleep(0.5)  
    return

def mean_squared_error(img1, img2):
    err_term = (img1.astype("float") - img2.astype("float"))
    error = np.sum(err_term * err_term)
    return error/float(img1.shape[0] * img2.shape[1])

if __name__ == "__main__":
    main()