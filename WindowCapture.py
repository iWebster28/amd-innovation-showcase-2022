# WindowCapture.py
# Utilities for capturing window state and screenshots.

from datetime import datetime
from time import sleep

import mss
from PIL import Image
from pywinauto.keyboard import send_keys
from pywinauto import Desktop
import win32clipboard as clip
from io import BytesIO

from constants import IMG_ERROR_THRESHOLD, OUTPUT_DIR, LAST_N_SCREENSHOTS

from WindowUtils import focus_window, get_win_name_from_user_input
from SliderUtils import *

class WindowCapture:
    def __init__(self):
        self.sct = mss.mss()

        self.target_win = None
        self.target_win_coords = None
        self.target_win_pngs = []

        self.onenote_win = None
        
    def set_target_win(self, target_win):
        self.target_win = target_win

    def set_target_win_coords(self, target_win_coords):
        self.target_win_coords = target_win_coords
    
    def set_onenote_win(self, onenote_win):
        self.onenote_win = onenote_win

    def set_window_of_interest(self, type="target_win", win_name=None, filter_by=None):
        # Get target window name
        while True:
            try:
                win_name = get_win_name_from_user_input(filter_by)
                # We should assure we are hooked into the correct window for every screenshot:
                # Hook into window to get its location and monitor
                win = Desktop(backend="uia").window(title=win_name, visible_only=False)
                if type == "target_win":
                    self.set_target_win(win)
                elif type == "onenote_win":
                    self.set_onenote_win(win)
                else:
                    raise Exception("Invalid window `type` specified.")
                break
            except Exception as e:
                print(f"Error: {e}")
                print("Please try selecting another window.")
        return
    
    def take_screenshot(self):
        """Screenshots the current `self.target_win"""
        # Screenshot window

        # with mss.mss() as sct: # may work if you unplug a monitor while slider is running
    
        print(f"Monitors found: {self.sct.monitors}") # First monitor (idx == 0) represents the "All in One" monitor
        monitor = {'left': self.target_win_coords[0], 'top': self.target_win_coords[1], 'width': self.target_win_coords[2] - self.target_win_coords[0], 'height': self.target_win_coords[3] - self.target_win_coords[1]}
        # output = f"./output/self.sct-{monitor['top']}x{monitor['left']}_{monitor['width']}x{monitor['height']}-{str(int(time()))}.png"

        # Grab the data
        sct_img = self.sct.grab(monitor)

        # Save to the picture file
        date_suffix = datetime.today().strftime("%m-%d-%Y %H_%M_%S")
        filename = f"./output/slide-{date_suffix}.png"

        # Save picture to file
        # mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)

        # Save picture to memory for analysis
        # Can also copy to clipboard if going to copy into onenote, or other notetaking app.
        target_win_png = mss.tools.to_png(sct_img.rgb, sct_img.size)
        self.target_win_pngs.append({"img_mem": target_win_png, "rgb": sct_img.rgb, "size": sct_img.size, "filename": filename})
        self.target_win_pngs = self.target_win_pngs[-LAST_N_SCREENSHOTS:] # Keep only the last 5 screenshots

        # filename = sct.shot(mon=0, output=f'./output/screenshot-{str(int(time()))}.png') # mon == -1 represents all monitors. https://python-mss.readthedocs.io/examples.html
        print(f"Diagnostic: Screenshot taken and stored at {filename}")

        for i, target_win_png in enumerate(self.target_win_pngs):
            print(f"Image {i}: size: {target_win_png['size']}, filename: {target_win_png['filename']}")

        # Go back to prev-focused window
        # print(prev_focused_win)
        # win32gui.SetActiveWindow(prev_focused_win)

        # send_keys('%{TAB}') # TODO: add a better way to do this so alt+tab doesn't get in the way
        return

    def save_new_screenshot(self):
        """Determines if the current screenshot is different from the previous screenshot(s), and if so, saves it to disk"""

        # Now: find the part of the window to focus on
        # Opencv? or use ML model? or use another method?

        # 1. Find area of interest in window. Crop screenshot to this.
        # 2. Compare screenshots based on similarity. (PNGs in memory)
        # 3. If different enough, save screenshot. (PNG saved to disk)
        # check for 2 screenshots of not. take second last and last to compare.

        if len(self.target_win_pngs) < 1:
            raise Exception("No screenshots taken: cannot save_new_screenshot().")

        error = 0
        cur_screen = Image.open(BytesIO(self.target_win_pngs[-1]['img_mem']))
        # cur_screen = self.target_win_pngs[-1]['img_mem']
        prev_screen = None

        if len(self.target_win_pngs) > 1:
            prev_screen = Image.open(BytesIO(self.target_win_pngs[-2]['img_mem']))
        
        # Get error between images
        if (cur_screen is not None) and (prev_screen is not None):
            error = mean_squared_error(np.array(cur_screen), np.array(prev_screen))
            print(f"Detected error in last 2 screens: {error}")
        
        # Save file if error is big enough
        if (error > IMG_ERROR_THRESHOLD) or (prev_screen is None):
            print("DETECTED FRAME CHANGE. SNAPPING!")
            # Save picture to file
            mss.tools.to_png(self.target_win_pngs[-1]['rgb'], self.target_win_pngs[-1]['size'], output=self.target_win_pngs[-1]['filename'])

            # Paste to OneNote
            if self.onenote_win != None:
                self.paste_to_onenote()
        return

    def paste_to_onenote(self):
        """Pastes the current `self.target_win_pngs` into the onenote window"""
        focus_window(self.onenote_win)

        # Reference: https://stackoverflow.com/questions/34322132/copy-image-to-clipboard
        image = Image.open(BytesIO(self.target_win_pngs[-1]['img_mem'])) # TODO: change: this may be inefficient. why are we using BytesIO twice? 
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        image_data = output.getvalue()[14:]
        output.close()
        clip.OpenClipboard()
        clip.EmptyClipboard()
        clip.SetClipboardData(clip.CF_DIB, image_data)
        clip.CloseClipboard()
        
        # Paste result into open OneNote page
        send_keys('^v')
        # Return focus to previously focused window
        send_keys('%{TAB}')
        return