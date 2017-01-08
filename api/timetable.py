import requests
from bs4 import BeautifulSoup
from api.section import Section


class Timetable:

    def __init__(self, term_year):
        self.url = 'https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest'
        self.sleep_time = 1
        self.base_request = {  # base required request data
            'BTN_PRESSED': 'FIND class sections',
            'TERMYEAR': term_year,
            'CAMPUS': '0',  # blacksburg campus
            'SCHDTYPE': '%'
        }
        self.data_keys = ['crn', 'code', 'name', 'lecture_type', 'credits', 'capacity',
                          'instructor', 'days', 'start_time', 'end_time', 'location', 'exam_type']

    def crn_lookup(self, crn_code, open_only=True):
        section = self.refined_lookup(crn_code=crn_code, open_only=open_only)
        return section[0] if section is not None else None

    def class_lookup(self, subject_code, class_number, open_only=True):
        return self.refined_lookup(subject_code=subject_code, class_number=class_number, open_only=open_only)

    def cle_lookup(self, cle_code, open_only=True):
        return self.refined_lookup(cle_code=cle_code, open_only=open_only)

    def subject_lookup(self, subject_code, open_only=True):
        return self.refined_lookup(subject_code=subject_code, open_only=open_only)

    def refined_lookup(self, crn_code=None, subject_code=None, class_number=None, cle_code=None, open_only=True):
        request_data = self.base_request.copy()
        if crn_code is not None:
            if len(crn_code) < 3:
                raise ValueError('Invalid CRN: must be longer than 3 characters')
            request_data['crn'] = crn_code
        if subject_code is not None:
            request_data['subj_code'] = subject_code
        if class_number is not None:
            if len(class_number) != 4:
                raise ValueError('Invalid Subject Number: must be 4 characters')
            request_data['CRSE_NUMBER'] = class_number
        if subject_code is None and class_number is not None:
            raise ValueError('A subject code must be supplied with a class number')
        request_data['CORE_CODE'] = 'AR%' if cle_code is None else cle_code
        request_data['open_only'] = 'on' if open_only else ''
        sections = self._parse_table(self._make_request(request_data))
        return None if sections is None or len(sections) == 0 else sections

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
