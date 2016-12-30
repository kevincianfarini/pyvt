from unittest import TestCase
from unittest.mock import patch
from api.timetable import TimetableUnavailableException


class TestTimetable(TestCase):
    pass


class TestTimetableException(TestCase):

    def setUp(self):
        self.e = TimetableUnavailableException("Test", 1)

    def test_timetable_unavailable_message(self):
        self.assertEqual("Test", str(self.e))

    def test_timetable_unavailable_exception_sleep_time(self):
        self.assertEqual(1, self.e.sleep_time)
