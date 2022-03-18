# main.py
# Slider CLI program.

from time import sleep

from WindowCapture import WindowCapture
from WindowState import WindowState
from WindowUtils import *

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
    print("\nDo you want to copy the screenshots directly into your current OneNote page? (y/n)", end=' ')
    if input().lower() == "y":
        capture.set_window_of_interest(type="onenote_win", filter_by="OneNote")
        
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
        capture.save_new_screenshot()

        # capture.crop_image() # future implementation for smarter video frame crops.

        sleep(MIN_SCREENSHOT_DELAY_SEC) # safety

    return


if __name__ == "__main__":
    main()