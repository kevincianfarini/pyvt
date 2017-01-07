from unittest import TestCase
from unittest.mock import patch
from api.timetable import TimetableUnavailableException, Timetable
from bs4 import BeautifulSoup
from api.section import Section


class TestTimetable(TestCase):

    def setUp(self):
        pass

    @patch('requests.post')
    def test_crn_lookup_simple(self, mock_post):
        pass

    def test_test(self):
        timetable = Timetable('201701')
        timetable.crn_lookup('17583', False)

    def test_crn_lookup_open_only_false(self):
        pass

    def test_crn_lookup_invalid_crn(self):
        timetable = Timetable('201701')
        with self.assertRaises(ValueError):
            timetable.crn_lookup('1')

    @patch('requests.post')
    def test_crn_lookup_raises_timetable_exception(self, mock_post):
        timetable = Timetable('201701')
        mock_post.return_value.status_code = 404
        with self.assertRaises(TimetableUnavailableException):
            timetable.crn_lookup('17583')
        self.assertEqual(2, timetable.sleep_time)
        self.assertNotIn('crn', timetable.base_request)

    def test_parse_table_single_entry(self):
        pass

    def test_parse_row_simple(self):
        with open('../test_data/test_row.html', 'r') as file:
            row = BeautifulSoup(file.read(), 'html.parser')
            t = Timetable('201701')
            data = t.parse_row(row)
            c = Section(crn='17583', code='STAT 4705', name='Statistics for Engr', lecture_type='L',
                        credits='3', capacity='60', instructor='GR Terrell',
                        days='TR', start_time='9:30AM', end_time='10:45AM', location='WMS 220', exam_type='09T')
            self.assertEqual(c, data)


class TestTimetableException(TestCase):

    def setUp(self):
        self.e = TimetableUnavailableException("Test", 1)

    def test_timetable_unavailable_message(self):
        self.assertEqual("Test", str(self.e))

    def test_timetable_unavailable_exception_sleep_time(self):
        self.assertEqual(1, self.e.sleep_time)
