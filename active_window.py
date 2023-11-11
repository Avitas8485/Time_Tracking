import time
import win32gui
import psutil
import win32process
import sqlite3




class ActiveWindowTracker:
    def __init__(self, db_name="window_tracker.db"):
        """Initializes the ActiveWindowTracker class"""
        self.current_window = None
        self.program_name = None
        self.start_time = time.time()
        self.active_time = 0

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
                start_time REAL,
                active_time REAL,
                program_name TEXT
            )
                       """)
        self.conn.commit()

                       

    def get_active_window_info(self):
        """Returns the title, exe, pid, and path of the currently active window"""
        try:
            pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
            return win32gui.GetWindowText(win32gui.GetForegroundWindow()), psutil.Process(pid[-1]).name(), pid[-1], psutil.Process(pid[-1]).cwd()
        except:
            return "None", "None", "None", "None"
        
    def track_active_window_time(self):
        """Returns the title and active time of the currently active window
        Returns:
            tuple: (title, exe, pid, path, active_time, program_name)"""
        active_window = self.get_active_window_info()
        program_name = active_window[0].split(" - ")[-1] if " - " in active_window[0] else active_window[0]
        #for now, skip the whole thing if the program name is "" or "None"
        if program_name == "" or program_name == "None":
            return self.current_window, self.active_time, program_name
        if active_window != self.current_window:
            if self.current_window is not None:
                self.active_time = time.time() - self.start_time
                print(f"{self.current_window[0]}, was active for {self.active_time:.2f} seconds")
            self.current_window = active_window
            self.start_time = time.time()
        time.sleep(0.5)
        return self.current_window, self.active_time, program_name

    def store_window_activity(self, title, exe, pid, path, active_time, program_name):
        """Store window activity in the database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO window_activity (title, exe, pid, path, start_time, active_time, program_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, exe, pid, path, self.start_time, active_time, program_name))
        self.conn.commit()

    def close_database_connection(self):
        """Closes the database connection"""
        self.conn.close()

def main():
    tracker = ActiveWindowTracker()
    try:
        while True:
            active_window, program_name, active_time = tracker.track_active_window_time()
            tracker.store_window_activity(*active_window, program_name, active_time)
    except KeyboardInterrupt:
        tracker.close_database_connection()
        print("Database connection closed")
        print("Program terminated")

if __name__ == "__main__":
    main()