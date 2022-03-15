# lists open windows
import enum
from pywinauto import Desktop

# Enumerate windows on Desktop
windows = Desktop(backend="uia").windows()

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

print(f"Capturing window with title \"{win_dict[target_win_idx]}\".")



