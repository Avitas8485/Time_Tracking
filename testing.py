import unittest
from unittest.mock import patch, Mock
import sqlite3
import time
from active_window import ActiveWindowTracker

class TestActiveWindowTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ActiveWindowTracker(db_name=":memory:")

    def test_init(self):
        self.assertEqual(self.tracker.current_window, None)
        self.assertEqual(self.tracker.program_name, None)
        self.assertIsInstance(self.tracker.start_time, float)
        self.assertEqual(self.tracker.active_time, 0)
        self.assertIsInstance(self.tracker.conn, sqlite3.Connection)

    @patch('sqlite3.connect')
    def test_connect_to_database(self, mock_connect):
        mock_connect.return_value = Mock(sqlite3.Connection)
        self.assertIsInstance(self.tracker.connect_to_database("test.db"), sqlite3.Connection)

    @patch('sqlite3.connect')
    def test_create_table(self, mock_connect):
        mock_connect.return_value = Mock(sqlite3.Connection)
        mock_connect.return_value.execute = Mock()
        self.tracker.create_table()
        mock_connect.return_value.execute.assert_called_once()

    def test_get_active_window_info(self):
        # This test would require mocking of several methods and external dependencies
        pass
        

    def test_get_idle_time(self):
        # This test would require mocking of external dependencies like win32api
        pass

    def test_is_idle(self):
        # This test would require mocking of the get_idle_time method
        pass

    @patch('sqlite3.connect')
    def test_store_window_activity(self, mock_connect):
        mock_connect.return_value = Mock(sqlite3.Connection)
        mock_connect.return_value.cursor = Mock()
        mock_connect.return_value.cursor.return_value.execute = Mock()
        self.tracker.store_window_activity("title", "exe", 123, "path", 10.0, "program", "12:00:00", "2022-01-01")
        mock_connect.return_value.cursor.return_value.execute.assert_called_once()

    def test_track_active_window_time(self):
        # This test would require mocking of several methods and external dependencies
        pass

    @patch('sqlite3.connect')
    def test_close_database_connection(self, mock_connect):
        mock_connect.return_value = Mock(sqlite3.Connection)
        mock_connect.return_value.close = Mock()
        self.tracker.close_database_connection()
        mock_connect.return_value.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()