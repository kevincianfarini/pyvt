from unittest import TestCase
from unittest.mock import patch
from api.timetable import TimetableError, Timetable
from bs4 import BeautifulSoup
from api.section import Section


class TestTimetableParsing(TestCase):

    def setUp(self):
        self.timetable = Timetable('201701')

    @patch('api.timetable.Timetable.parse_row')
    def test_parse_table_single_entry(self, mock_row):
        with open('./test_data/test_crn_request_table.html', 'r') as file:
            bs = BeautifulSoup(file.read(), 'html.parser')
            self.timetable.parse_table(bs)
            mock_row.assert_called_once()

    def test_parse_row_simple(self):
        with open('./test_data/test_row.html', 'r') as file:
            row = BeautifulSoup(file.read(), 'html.parser')
            data = self.timetable.parse_row(row)
            c = Section(crn='17583', code='STAT 4705', name='Statistics for Engr', lecture_type='L',
                        credits='3', capacity='60', instructor='GR Terrell',
                        days='T R', start_time='9:30AM', end_time='10:45AM', location='WMS 220', exam_type='09T')
            self.assertEqual(c, data)


class TestTimetableCrnLookup(TestCase):

    def setUp(self):
        self.timetable = Timetable('201701')

    @patch('requests.post')
    @patch('api.timetable.Timetable.parse_table')
    def test_crn_lookup_simple(self, mock_table, mock_post):
        with open('./test_data/test_crn_request_no_open_sections.html', 'r') as file:
            mock_post.return_value.status_code = 200
            mock_post.return_value.content = file.read()
            mock_table.return_value = []
            self.assertIsNone(self.timetable.crn_lookup('17582', False))
            mock_post.assert_called_once()

    @patch('requests.post')
    @patch('api.timetable.Timetable.parse_table')
    def test_crn_lookup_open_only_false(self, mock_parse, mock_post):
        with open('./test_data/test_crn_request_open_only_false.html', 'r') as file:
            mock_post.return_value.status_code = 200
            mock_post.return_value.content = file.read()
            self.timetable.crn_lookup('17583', False)
            mock_parse.assert_called_once()

    def test_crn_lookup_invalid_crn(self):
        with self.assertRaises(ValueError):
            self.timetable.crn_lookup('1')

    @patch('requests.post')
    def test_crn_lookup_raises_timetable_exception(self, mock_post):
        mock_post.return_value.status_code = 404
        with self.assertRaises(TimetableError):
            self.timetable.crn_lookup('17583')
        self.assertEqual(2, self.timetable.sleep_time)
        self.assertNotIn('crn', self.timetable.base_request)


class TestTimetableClassLookup(TestCase):

    def setUp(self):
        self.timetable = Timetable('201701')
        

class TestTimetableError(TestCase):

    def setUp(self):
        self.e = TimetableError("Test", 1)

    def test_timetable_unavailable_message(self):
        self.assertEqual("Test", str(self.e))

    def test_timetable_unavailable_exception_sleep_time(self):
        self.assertEqual(1, self.e.sleep_time)
