# constants.py

# Windows
WIN_FOCUS_TRIES = 5                 # Number of times to try to focus window
WIN_FOCUS_TIMEOUT_SEC = 5           # Time before we give up on focusing a window
WINDOW_RESIZE_TIMEOUT_SEC = 0.1     # Timeout to ensure window visable before screenshotting a window

# Screenshots
OUTPUT_DIR = "output"
LAST_N_SCREENSHOTS = 5
MIN_SCREENSHOT_DELAY_SEC = 1        # Minimum time between screenshots
IMG_ERROR_THRESHOLD = 1500          # Threshold for image similarity