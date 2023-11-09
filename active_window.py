import time
import win32gui
import psutil
import win32process







def get_active_window_info():
    """Returns the title, exe, pid, and path of the currently active window"""
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return win32gui.GetWindowText(win32gui.GetForegroundWindow()), psutil.Process(pid[-1]).name(), pid[-1], psutil.Process(pid[-1]).cwd()
    except:
        return "None"



def track_active_window_time():
    current_window = None
    start_time = time.time()

    while True:
        active_window = get_active_window_info()
        if active_window != current_window:
            if current_window is not None:
                print(f"{current_window[0]} was active for {time.time() - start_time} seconds")
            current_window = active_window
            start_time = time.time()
        time.sleep(0.1)
        


if __name__ == "__main__":
    track_active_window_time()

