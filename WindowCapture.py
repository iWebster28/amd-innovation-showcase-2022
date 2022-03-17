# General
from datetime import datetime

import mss
from pywinauto.keyboard import send_keys
from pywinauto import Desktop

from WindowUtils import focus_window, get_win_name_from_user_input

class WindowCapture:
    def __init__(self):
        self.target_win = None
        self.target_win_coords = None
        self.target_win_png = None

        self.onenote_win = None
    
    def set_target_win(self, target_win):
        self.target_win = target_win

    def set_target_win_coords(self, target_win_coords):
        self.target_win_coords = target_win_coords
    
    def set_onenote_win(self, onenote_win):
        self.onenote_win = onenote_win

    def set_window_of_interest(self, type="target_win", win_name=None):
        # Get target window name
        while True:
            try:
                win_name = get_win_name_from_user_input()
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

            # Save picture to file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
            # Save picture to memory
            self.target_win_png = mss.tools.to_png(sct_img.rgb, sct_img.size)

            # Can also copy to clipboard if going to copy into onenote, or other notetaking app.
            # Keep in memory for analysis.

            # filename = sct.shot(mon=0, output=f'./output/screenshot-{str(int(time()))}.png') # mon == -1 represents all monitors. https://python-mss.readthedocs.io/examples.html
            print(filename)

        # Go back to prev-focused window
        # print(prev_focused_win)
        # win32gui.SetActiveWindow(prev_focused_win)
        send_keys('%{TAB}')
        return

    def paste_to_onenote(self):
        """Pastes the current `self.target_win_png` into the onenote window"""
        # focus_window(self.onenote_win)

        # send_keys('%{TAB}')
        raise NotImplementedError