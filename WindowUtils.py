# WindowUtils.py
# Utilities for window capture.

# General
from time import sleep

from pywinauto import Desktop

# Constants
from constants import *

def get_win_name_from_user_input():
    """
    Returns:
        window name: the name of the window to capture.
    """
    win_dict = get_window_dict()

    # Wait for window name to be selected
    wait_on_input = True
    while wait_on_input:
        try:
            win_idx = int(input('Which window do you want to capture? (enter index)\n'))
            # Check if index is valid
            if win_idx < 0 or win_idx >= len(win_dict):
                wait_on_input = True
                raise Exception("Invalid index.")
            else:
                wait_on_input = False
        except Exception:
            print(f"Please enter a value in range 0-{len(win_dict.keys()) - 1}.")
            wait_on_input = True

    # Return target window name
    win_name = win_dict[win_idx]
    print(f"Capturing window with title \"{win_name}\".")
    return win_name


def get_window_dict():
    """
    Returns:
        dict: Dictionary of window index (on Desktop) and name
    """

    # Enumerate windows on Desktop
    windows = Desktop(backend="uia").windows()
    # print(windows)

    # Create dictionary of window index and name
    exemption_list = [None, '', 'Program Manager', 'Taskbar', 'NVIDIA GeForce Overlay'] # Window names to ignore
    windows = [w for w in windows if w.window_text() not in exemption_list]
    win_dict = {idx: w.window_text() for idx, w in enumerate(windows)}

    # List windows
    print("Windows found:")
    for idx, win_name in win_dict.items():
        print(f"{idx}: {win_name}")
    
    return win_dict
        
def focus_window(window):
    """Focuses `window`. Returns `True` on success, `False` on failure."""
    count = 1
    while count <= WIN_FOCUS_TRIES:
        try:
            # target_win.restore()
            window.set_focus()
            return True
        except Exception as e:
            print(f"Error: {e}")
            print(f"Window could not be focused. Attempt {count} of {WIN_FOCUS_TRIES}.")
            sleep(WIN_FOCUS_TIMEOUT_SEC)
            if count == WIN_FOCUS_TRIES:
                return False
            count += 1
    return False