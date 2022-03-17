# General
from datetime import datetime

import mss
from pywinauto.keyboard import send_keys

class WindowCapture:
    def __init__(self):
        self.target_win = None
        self.target_win_coords = None
    
    def set_target_win(self, target_win):
        self.target_win = target_win

    def set_target_win_coords(self, target_win_coords):
        self.target_win_coords = target_win_coords
    
    def screenshot(self):
        """Screenshots the current `self.target_win"""
        # Screenshot window
        with mss.mss() as sct:
            print(f"Monitors found: {sct.monitors}") # First monitor (idx == 0) represents the "All in One" monitor
            monitor = {'left': self.target_win_coords[0], 'top': self.target_win_coords[1], 'width': self.target_win_coords[2] - self.target_win_coords[0], 'height': self.target_win_coords[3] - self.target_win_coords[1]}
            # output = f"./output/sct-{monitor['top']}x{monitor['left']}_{monitor['width']}x{monitor['height']}-{str(int(time()))}.png"

            # Grab the data
            sct_img = sct.grab(monitor)

            # Save to the picture file
            date_suffix = datetime.today().strftime("%m-%d-%Y %H_%M_%S")
            filename = f"./output/slide-{date_suffix}.png"
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)

            # Can also copy to clipboard if going to copy into onenote, or other notetaking app.
            # Keep in memory for analysis.

            # filename = sct.shot(mon=0, output=f'./output/screenshot-{str(int(time()))}.png') # mon == -1 represents all monitors. https://python-mss.readthedocs.io/examples.html
            print(filename)

        # Go back to prev-focused window
        # print(prev_focused_win)
        # win32gui.SetActiveWindow(prev_focused_win)
        send_keys('%{TAB}')
