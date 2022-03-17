# General
from time import sleep

from pywinauto import Desktop

from WindowCapture import WindowCapture
from WindowState import WindowState

# Constants
TARGET_WIN_FOCUS_TRIES = 5
TARGET_WIN_FOCUS_TIMEOUT_SEC = 5
WINDOW_RESIZE_TIMEOUT_SEC = 0.1 # Timeout to ensure window visable before screenshotting a window

def main():
    """Start slider.
    """
    slider_running = True

    # Init our WindowCapture object
    capture = WindowCapture()

    # Get target window name
    while True:
        try:
            target_win_name = get_target_win_name_from_user_input()
            # We should assure we are hooked into the correct window for every screenshot:
            # Hook into window to get its location and monitor
            target_win = Desktop(backend="uia").window(title=target_win_name, visible_only=False)
            capture.set_target_win(target_win)
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try selecting another window.")
        
    # Get currently focused window
    # prev_focused_win = win32gui.GetForegroundWindow()
    # prev_focused_win = Desktop(backend="win32").has_focus()
    # just use alt+tab later!

    # Capture screenshots
    while slider_running:
        # Focus window
        count = 1
        while count <= TARGET_WIN_FOCUS_TRIES:
            try:
                # target_win.restore()
                capture.target_win.set_focus()
                break
            except Exception as e:
                print(f"Error: {e}")
                print(f"Window could not be focused. Attempt {count} of {TARGET_WIN_FOCUS_TRIES}.")
                sleep(TARGET_WIN_FOCUS_TIMEOUT_SEC)
                if count == TARGET_WIN_FOCUS_TRIES:
                    print("Exiting slider.")
                    exit(1)
                count += 1
        
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
        capture.screenshot()

        # Determining important frames to save!
        # Now: find the part of the window to focus on
        # Opencv? or use ML model? or use another method?

        # 1. Find area of interest in window. Crop screenshot to this.
        # 2. Compare screenshots based on similarity. (PNGs in memory)
        # 3. If different enough, save screenshot. (PNG saved to disk)


    return


def get_target_win_name_from_user_input():
    """
    Returns:
        window name: the name of the window to capture.
    """
    win_dict = get_window_dict()

    # Wait for window name to be selected
    wait_on_input = True
    while wait_on_input:
        try:
            target_win_idx = int(input('Which window do you want to capture? (enter index)\n'))
            # Check if index is valid
            if target_win_idx < 0 or target_win_idx >= len(win_dict):
                wait_on_input = True
                raise Exception("Invalid index.")
            else:
                wait_on_input = False
        except Exception:
            print(f"Please enter a value in range 0-{len(win_dict.keys()) - 1}.")
            wait_on_input = True

    # Return target window name
    target_win_name = win_dict[target_win_idx]
    print(f"Capturing window with title \"{target_win_name}\".")
    return target_win_name


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


if __name__ == "__main__":
    main()