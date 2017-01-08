import requests
from bs4 import BeautifulSoup
from api.section import Section
# request_data = {
#     'TERMYEAR': '201701',
#     'CAMPUS': '0',
#     'CORE_CODE': 'AR%',
#     # 'subj_code': 'STAT',
#     'SCHDTYPE': '%',
#     # 'CRSE_NUMBER': '4705',
#     'crn': '17583',
#     'open_only': '',
#     'BTN_PRESSED': 'FIND class sections'
# }


class Timetable:

    def __init__(self, term_year):
        self.url = 'https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest'
        self.sleep_time = 1
        self.base_request = { #base required request data
            'BTN_PRESSED': 'FIND class sections',
            'TERMYEAR': term_year,
            'CAMPUS': '0', #blacksburg campus
            'CORE_CODE': 'AR%',
            'SCHDTYPE': '%'
        }
        self.data_keys = ['crn', 'code', 'name', 'lecture_type', 'credits', 'capacity',
                          'instructor', 'days', 'start_time', 'end_time', 'location', 'exam_type']

    def crn_lookup(self, crn_code, open_only=True):
        if len(crn_code) < 3:
            raise ValueError('Invalid CRN: must be longer than 3 characters')
        request_data = self.base_request.copy()
        request_data['crn'] = crn_code
        request_data['open_only'] = 'on' if open_only else ''
        section = self._parse_table(self._make_request(request_data))
        return None if section is None or len(section) == 0 else section[0]

    def class_lookup(self, subject_code, class_number, open_only=True):
        request_data = self.base_request.copy()
        request_data['subj_code'] = subject_code
        request_data['CRSE_NUMBER'] = class_number

    def cle_lookup(self, cle_code, open_only=True):
        pass

    def subject_lookup(self, subject_code, open_only=True):
        pass

    def _parse_row(self, row):
        entries = [entry.text.replace('\n', '').replace('-', ' ').strip() for entry in row.find_all('td')]
        return Section(**dict(zip(self.data_keys, entries)))

    def _parse_table(self, html):
        table = html.find('table', attrs={'class': 'dataentrytable'})
        if table is None:
            return None
        rows = [row for row in table.find_all('tr') if row.attrs == {}]
        sections = [self._parse_row(c) for c in rows]
        return sections

    def _make_request(self, request_data):
        r = requests.post(self.url, data=request_data)
        if r.status_code != 200:
            self.sleep_time *= 2
            raise TimetableError('The VT Timetable is down or the request was bad.',
                                 self.sleep_time)
        return BeautifulSoup(r.content, 'html.parser')


class TimetableError(Exception):

    def __init__(self, message, sleep_time):
        super(TimetableError, self).__init__(message)
        self.sleep_time = sleep_time
