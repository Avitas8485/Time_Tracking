import time
import win32gui
import psutil
import win32process
import sqlite3
import win32api
import logging
import datetime


class ActiveWindowTracker:
    def __init__(self, db_name="window_tracker.db"):
        """Initializes the ActiveWindowTracker class"""
        self.current_window = None
        self.program_name = None
        self.start_time = time.time()
        self.active_time = 0
        self.idle_threshold = 60
        

        self.conn = sqlite3.connect(db_name)
        self.create_table()
        

    def create_table(self):
        """Creates a table in the database to store the active window information"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS window_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                exe TEXT,
                pid INTEGER,
                path TEXT,
                start_time TEXT,
                start_date TEXT,
                active_time REAL,
                program_name TEXT
            )
                       """)
        self.conn.commit()
                       

    def get_active_window_info(self):
        """Returns the title, exe, pid, and path of the currently active window"""
        try:
            pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
            process = psutil.Process(pid[-1])
            return win32gui.GetWindowText(win32gui.GetForegroundWindow()), process.name(), pid[-1], process.cwd()
        except Exception as e:
            logging.error(f"Error getting active window info: {e}")
            return "None", "None", "None", "None"
        

    def get_idle_time(self):
        """Returns the idle time in seconds"""
        last_input = win32api.GetLastInputInfo()
        curr_ticks = win32api.GetTickCount()
        idle_time = (curr_ticks - last_input) / 1000.0
        return idle_time
    
    
    def is_idle(self):
        """Returns True if the user is idle, False otherwise"""
        return self.get_idle_time() > self.idle_threshold

    def store_window_activity(self, title, exe, pid, path, active_time, program_name, start_time, start_date):
        """Store window activity in the database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO window_activity (title, exe, pid, path, start_time, start_date, active_time, program_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, exe, pid, path, start_time, start_date, active_time, program_name))
        self.conn.commit()

    def track_active_window_time(self):
        """Returns the title and active time of the currently active window
        Returns:
            tuple: (title, exe, pid, path, active_time, program_name)"""
        if self.is_idle():
            self.current_window = "idle", "idle", "idle", "idle"
            self.start_time = time.time()
            self.program_name = "idle"
            time.sleep(5)
            return self.current_window, self.active_time, self.program_name
        
        active_window = self.get_active_window_info()
        self.program_name = active_window[0].split(" - ")[-1] if " - " in active_window[0] else active_window[0]
        
        if active_window != self.current_window:
            # Window has changed
            # to prevent the database from storing explorer.exe as the active window
            if active_window[0] == "" or active_window[0] == "None":
                pass
            if self.current_window is not None and self.current_window[0] != "":
                self.active_time = time.time() - self.start_time
                print(f"{self.current_window[0]}, was active for {self.active_time:.2f} seconds")
                self.active_time = round(self.active_time, 2)
                start_time = datetime.datetime.now().strftime("%H:%M:%S")
                start_date = datetime.datetime.now().strftime("%Y-%m-%d")
                self.store_window_activity(*self.current_window, active_time=self.active_time, program_name=self.program_name, start_time=start_time, start_date=start_date)
            self.current_window = active_window
            self.start_time = time.time()
        time.sleep(1)
        return self.current_window, self.active_time, self.program_name


    


    def close_database_connection(self):
        """Closes the database connection"""
        self.conn.close()



def main():
    tracker = ActiveWindowTracker()
    try:
        while True:
            tracker.track_active_window_time()
            
    except KeyboardInterrupt:
        tracker.close_database_connection()
        print("Database connection closed")
        print("Program terminated")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()