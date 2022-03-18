# General
from time import sleep

from pywinauto import Desktop

from WindowCapture import WindowCapture
from WindowState import WindowState
from WindowUtils import *

# Constants
from constants import *

def main():
    """
    Start slider.
    """
    slider_running = True

    # Init our WindowCapture object
    capture = WindowCapture()

    # Set window of interest
    capture.set_window_of_interest(type="target_win")
    print("\nDo you want to copy the screenshots directly into your current OneNote page? (y/n)")
    if input().lower() == "y":
        capture.set_window_of_interest(type="onenote_win")
        
    # Get currently focused window
    # prev_focused_win = win32gui.GetForegroundWindow()
    # prev_focused_win = Desktop(backend="win32").has_focus()
    # just use alt+tab later!

    # Capture screenshots
    while slider_running:
        # Focus window
        focused = focus_window(capture.target_win)
        if not focused:
            print("Exiting slider.")
            exit(1)
        
        # If window was minimized prior, we need time for it to restore from set_focus() before we screenshot it.
        count = 0
        while capture.target_win.get_show_state() == WindowState.MINIMIZED: # max/min/restore = 1/2/3
            sleep(WINDOW_RESIZE_TIMEOUT_SEC)
            print("Waiting for window restore...")
            if count == 10:
                print("Window remains minimized; cannot capture. Exiting slider.")
                exit(1)
            
        # Get window coords
        target_win_loc = capture.target_win.rectangle()
        capture.set_target_win_coords([target_win_loc.left, target_win_loc.top, target_win_loc.right, target_win_loc.bottom])
        # print(target_win_loc)
        # print(target_win_coords)

        # Capture screenshot
        capture.take_screenshot()

        # Determining important frames to save!
        # Now: find the part of the window to focus on
        # Opencv? or use ML model? or use another method?

        # 1. Find area of interest in window. Crop screenshot to this.
        # 2. Compare screenshots based on similarity. (PNGs in memory)
        # 3. If different enough, save screenshot. (PNG saved to disk)
        capture.save_new_screenshot()

        sleep(MIN_SCREENSHOT_DELAY_SEC) #safety


    return


if __name__ == "__main__":
    main()