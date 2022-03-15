from datetime import datetime

# Screenshot util
import mss

# lists open windows
from pywinauto import Desktop

# Enumerate windows on Desktop
windows = Desktop(backend="uia").windows()
# print(windows)

exemption_list = [None, '', 'Program Manager', 'Taskbar', 'NVIDIA GeForce Overlay'] # Window names to ignore

windows = [w for w in windows if w.window_text() not in exemption_list]
win_dict = {idx: w.window_text() for idx, w in enumerate(windows)}

print("Windows found:")
for idx, win_name in win_dict.items():
    print(f"{idx}: {win_name}")

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
        print(f"Please enter a value in range 0-{len(windows) - 1}.")
        wait_on_input = True

target_win_name = win_dict[target_win_idx]
print(f"Capturing window with title \"{target_win_name}\".")

# Hook into window to get its location and monitor
target_win = Desktop(backend="uia").window(title=target_win_name)
target_win_loc = target_win.rectangle()
print(target_win_loc)
target_win_coords = [target_win_loc.left, target_win_loc.top, target_win_loc.right, target_win_loc.bottom]
print(target_win_coords)

# Screenshot window
with mss.mss() as sct:
    # TODO: ensure non-primary monitors work
    
    print(f"Monitors found: {sct.monitors}") # First monitor (idx == 0) represents the "All in One" monitor
    monitor = {'top': target_win_coords[0], 'left': target_win_coords[1], 'width': target_win_coords[2], 'height': target_win_coords[3]}
    # output = f"./output/sct-{monitor['top']}x{monitor['left']}_{monitor['width']}x{monitor['height']}-{str(int(time()))}.png"
    date_suffix = datetime.today().strftime("%m-%d-%Y %H_%M_%S")
    filename = f"./output/slide-{date_suffix}.png"

    # Grab the data
    sct_img = sct.grab(monitor)

    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)

    # filename = sct.shot(mon=0, output=f'./output/screenshot-{str(int(time()))}.png') # mon == -1 represents all monitors. https://python-mss.readthedocs.io/examples.html
    print(filename)





