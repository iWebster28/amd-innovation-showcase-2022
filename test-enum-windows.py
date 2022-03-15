# lists open windows
from pywinauto import Desktop

windows = Desktop(backend="uia").windows()

exemption_list = [None, '', 'Program Manager', 'Taskbar', 'NVIDIA GeForce Overlay'] # Window names to ignore

windows = [w for w in windows if w.window_text() not in exemption_list]
win_dict = {idx: w.window_text() for idx, w in enumerate(windows)}
print(win_dict)

print("Windows found:")
for idx, win_name in win_dict.items():
    print(f"{idx}: {win_name}")

target_win_idx = int(input('Which window do you want to capture? (enter index)\n'))
print(f"Capturing window with title \"{win_dict[target_win_idx]}\".")



