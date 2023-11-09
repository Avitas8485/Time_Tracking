import time
import win32gui
import psutil
import win32process





class ActiveWindowTracker:
    def __init__(self):
        self.current_window = None
        self.start_time = time.time()
        self.active_time = 0

    def get_active_window_info(self):
        """Returns the title, exe, pid, and path of the currently active window"""
        try:
            pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
            return win32gui.GetWindowText(win32gui.GetForegroundWindow()), psutil.Process(pid[-1]).name(), pid[-1], psutil.Process(pid[-1]).cwd()
        except:
            return "None"
        
    def track_active_window_time(self):
        """Returns the title and active time of the currently active window"""
        active_window = self.get_active_window_info()
        if active_window != self.current_window:
            if self.current_window is not None:
                self.active_time = time.time() - self.start_time
                print(f"{self.current_window[0]} was active for {self.active_time:.2f} seconds")
            self.current_window = active_window
            self.start_time = time.time()
        time.sleep(0.1)
        return self.current_window[0], self.active_time


if __name__ == "__main__":
    tracker = ActiveWindowTracker()
    while True:
        tracker.track_active_window_time()