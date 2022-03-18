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
        self.target_win_pngs.append({"img_mem": target_win_png, "rgb": sct_img.rgb, "size": sct_img.size, "filename": filename, "sct": sct_img})
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
    
    def crop_image(self):
        """Not Implemented"""
        raise NotImplementedError

        import cv2

        # load the image
        # image = cv2.imread(BytesIO(self.target_win_pngs[-1]['img_mem']), 1)
        image = np.array(self.target_win_pngs[-1]['sct']) # or pass sct  from sct.grab

        # https://stackoverflow.com/questions/44588279/find-and-draw-the-largest-contour-in-opencv-on-a-specific-color-python#:~:text=You%20can%20start%20by%20defining,rectangular%20shape%20of%20the%20book.&text=If%20you%20want%20the%20book,you%20can%20find%20it%20here.

        # # red color boundaries [B, G, R]
        # lower = [1, 0, 20]
        # upper = [60, 40, 220]

        # # create NumPy arrays from the boundaries
        # lower = np.array(lower, dtype="uint8")
        # upper = np.array(upper, dtype="uint8")

        # # find the colors within the specified boundaries and apply
        # # the mask
        # mask = cv2.inRange(image, lower, upper)
        # output = cv2.bitwise_and(image, image, mask=mask)

        # ret,thresh = cv2.threshold(mask, 40, 255, 0)
        # if (cv2.__version__[0] > 3):
        #     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # else:
        #     im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # if len(contours) != 0:
        #     # draw in blue the contours that were founded
        #     cv2.drawContours(output, contours, -1, 255, 3)

        #     # find the biggest countour (c) by the area
        #     c = max(contours, key = cv2.contourArea)
        #     x,y,w,h = cv2.boundingRect(c)

        #     # draw the biggest contour (c) in green
        #     cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

        # # show the images
        # cv2.imshow("Result", np.hstack([image, output]))

        # cv2.waitKey(0)

        # im = cv2.imread('test.jpg')
        imgray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(imgray, 10, 255, cv2.THRESH_BINARY_INV)
        # th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # print(contours)





        if len(contours) != 0:
            # draw in blue the contours that were founded
            cv2.drawContours(image, contours, -1, 255, 3)

            # find the biggest countour (c) by the area
            c = max(contours, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)

            # draw the biggest contour (c) in green
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

        # show the images
        cv2.imshow("Result", np.hstack([image]))
        cv2.waitKey(0)
        exit(0)
    