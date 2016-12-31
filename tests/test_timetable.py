from unittest import TestCase
from unittest.mock import patch
from api.timetable import TimetableUnavailableException, Timetable


class TestTimetable(TestCase):

    def setUp(self):
        pass

    @patch('requests.post')
    def test_crn_lookup_simple(self):
        pass

    def test_crn_lookup_open_only_false(self):
        pass

    def test_crn_lookup_invalid_crn(self):
        pass

    @patch('requests.post')
    def test_crn_lookup_raises_timetable_exception(self, mock_post):
        timetable = Timetable('201701')
        mock_post.return_value.status_code = 404
        with self.assertRaises(TimetableUnavailableException):
            timetable.crn_lookup('17583')
        self.assertEqual(2, timetable.sleep_time)


class TestTimetableException(TestCase):

    def setUp(self):
        self.e = TimetableUnavailableException("Test", 1)

    def test_timetable_unavailable_message(self):
        self.assertEqual("Test", str(self.e))

    def test_timetable_unavailable_exception_sleep_time(self):
        self.assertEqual(1, self.e.sleep_time)
