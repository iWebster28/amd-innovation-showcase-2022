# SliderUtils.py
# Utility functions for slider functionality.

import numpy as np
import os
import glob

def mean_squared_error(img1, img2):
    try:
        err_term = (img1.astype("float") - img2.astype("float"))
    except Exception:
        raise Exception("MSE failure.")
    error = np.sum(err_term * err_term)
    return error/float(img1.shape[0] * img2.shape[1]) # we should return a value ratio that is proportional to window size!

def remove_all_in_dir(dir):
    """Removes all files in directory `dir`

    Args:
        dir (str): directory to remove all files in
    """
    for file in glob.glob(os.path.join(dir, "*")):
        os.remove(file)
    return