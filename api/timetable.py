import requests
from bs4 import BeautifulSoup
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
        self.base_request = {
            'BTN_PRESSED': 'FIND class sections',
            'TERMYEAR': term_year,
            'CAMPUS': '0', #blacksburg campus
            'CORE_CODE': 'AR%',
            'SCHDTYPE': '%'
        }

    def crn_lookup(self, crn_code, open_only=True):
        if len(crn_code) < 3:
            raise ValueError('Invalid CRN: must be longer than 3 characters')
        request_data = self.base_request.copy()
        request_data['crn'] = crn_code
        request_data['open_only'] = 'on' if open_only else ''
        r = requests.post(self.url, data=request_data)
        if r.status_code != 200:
            self.sleep_time *= 2
            raise TimetableUnavailableException('The VT Timetable is down or the request was bad.',
                                                self.sleep_time)
        bs = BeautifulSoup(r.content, 'html.parser')
        print(r.text)


    def class_lookup(self, class_code, open_only=True):
        pass

    def cle_lookup(self, cle_code, open_only=True):
        pass

    def subject_lookup(self, subject_code, open_only=True):
        pass


class TimetableUnavailableException(Exception):

    def __init__(self, message, sleep_time):
        super(TimetableUnavailableException, self).__init__(message)
        self.sleep_time = sleep_time
