import unittest
import sqlite3
import os
from active_window import ActiveWindowTracker

class TestActiveWindowTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ActiveWindowTracker("test.db")

    def tearDown(self):
        self.tracker.close_database_connection()
        os.remove("test.db")

    def test_create_database(self):
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='window_activity'")
        self.assertIsNotNone(cursor.fetchone())
        conn.close()

    def test_get_active_window_info(self):
        self.assertNotEqual(self.tracker.get_active_window_info(), ("None", "None", "None", "None"))

    def test_track_active_window_time(self):
        self.assertIsNotNone(self.tracker.track_active_window_time())

    def test_store_window_activity(self):
        self.tracker.store_window_activity("title", "exe", 123, "path", 1.23, "program_name")
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM window_activity")
        self.assertIsNotNone(cursor.fetchone())
        conn.close()

    def test_close_database_connection(self):
        self.tracker.close_database_connection()
        with self.assertRaises(sqlite3.ProgrammingError):
            self.tracker.conn.execute("SELECT * FROM window_activity")

if __name__ == "__main__":
    unittest.main()

    