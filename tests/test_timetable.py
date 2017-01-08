from unittest import TestCase
from unittest.mock import patch
from api.timetable import TimetableError, Timetable
from bs4 import BeautifulSoup
from api.section import Section


class TestTimetableHelpers(TestCase):

    def setUp(self):
        self.timetable = Timetable('201701')

    @patch('api.timetable.Timetable._parse_row')
    def test_parse_table_single_entry(self, mock_row):
        with open('./tests/test_data/test_crn_request_table.html', 'r') as file:
            bs = BeautifulSoup(file.read(), 'html.parser')
            self.timetable._parse_table(bs)
            mock_row.assert_called_once()

    @patch('api.timetable.Timetable._parse_row')
    def test_parse_table_no_results(self, mock_row):
        with open('./tests/test_data/test_table_no_results.html', 'r') as file:
            table = BeautifulSoup(file.read(), 'html.parser')
            self.assertIsNone(self.timetable._parse_table(table))
            mock_row.assert_not_called()

    def test_parse_row_simple(self):
        with open('./tests/test_data/test_row.html', 'r') as file:
            row = BeautifulSoup(file.read(), 'html.parser')
            data = self.timetable._parse_row(row)
            c = Section(crn='17583', code='STAT 4705', name='Statistics for Engr', lecture_type='L',
                        credits='3', capacity='60', instructor='GR Terrell',
                        days='T R', start_time='9:30AM', end_time='10:45AM', location='WMS 220', exam_type='09T')
            self.assertEqual(c, data)

    @patch('requests.post')
    def test_make_request_bad_status(self, mock_post):
        mock_post.return_value.status_code = 400
        with self.assertRaises(TimetableError):
            self.timetable._make_request({'dummy': 'data'})
        self.assertEqual(2, self.timetable.sleep_time)

    @patch('requests.post')
    def test_make_request_simple(self, mock_post):
        mock_post.return_value.content = '<html></html>'
        mock_post.return_value.status_code = 200
        self.assertTrue(isinstance(self.timetable._make_request({'dummy': 'data'}), BeautifulSoup))


class TestTimetableLookups(TestCase):

    def setUp(self):
        self.timetable = Timetable('201701')

    def test_crn_lookup_bad_value(self):
        with self.assertRaises(ValueError):
            self.timetable.crn_lookup('1')

    @patch('api.timetable.Timetable._make_request')
    @patch('api.timetable.Timetable._parse_table')
    def test_crn_no_results(self, mock_parse, mock_request):
        with open('./tests/test_data/test_crn_request_no_open_sections.html', 'r') as file:
            bs = BeautifulSoup(file.read(), 'html.parser')
            mock_request.return_value = bs
            self.timetable.crn_lookup('17583')
            mock_parse.assert_called_once_with(bs)

    @patch('api.timetable.Timetable._parse_table')
    @patch('requests.post')
    def test_crn_returns_none(self, mock_post, mock_parse):
        mock_parse.return_value = None
        mock_post.return_value.status_code = 200
        mock_post.return_value.content = '<html></html>'
        self.assertIsNone(self.timetable.crn_lookup('17583'))
        mock_parse.return_value = []
        self.assertIsNone(self.timetable.crn_lookup('17583'))

    @patch('api.timetable.Timetable._parse_table')
    @patch('requests.post')
    def test_crn_returns_section(self, mock_post, mock_parse):
        mock_parse.return_value = [Section(dummy='data')]
        mock_post.return_value.status_code = 200
        mock_post.return_value.content = '<html></html>'
        self.assertEqual(Section(dummy='data'), self.timetable.crn_lookup('17583'))


class TestTimetableError(TestCase):

    def setUp(self):
        self.e = TimetableError("Test", 1)

    def test_timetable_unavailable_message(self):
        self.assertEqual("Test", str(self.e))

    def test_timetable_unavailable_exception_sleep_time(self):
        self.assertEqual(1, self.e.sleep_time)
