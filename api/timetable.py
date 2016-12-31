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
#
# r = requests.post('https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest', data=request_data)
# bs = BeautifulSoup(r.content, 'html.parser')
# print()

class Timetable:
    # TODO get basic functionality working then work on schedule type requests
    def __init__(self, term_year):
        self.url = 'https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest'
        self.sleep_time = 1
        self.base_request = {
            'BTN_PRESSED': 'FIND class sections',
            'TERMYEAR': term_year,
            'CAMPUS': '0' #blacksburg campus
        }

    def crn_lookup(self, crn_code, open_only=True):
        request_data = self.base_request
        request_data['crn'] = crn_code
        r = requests.post(self.url, data=request_data)
        if r.status_code != 200:
            self.sleep_time *= 2
            raise TimetableUnavailableException('The VT Timetable seems to be unavailable at the moment',
                                                self.sleep_time)

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
