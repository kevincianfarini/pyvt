from unittest import TestCase
from api.classes import Class


class TestClass(TestCase):

    def test_str(self):
        c = Class(17583, 'Statistics for Engineers', False,
                  ('T', 'R'), "9:30am", 'spr17')

        self.assertEqual("Statistics for Engineers (17583) on (T, R) at 9:30am",
                         str(c))

    def test_days_str(self):
        c = Class(17583, 'Statistics for Engineers', False,
                  ('T', 'R'), "9:30am", 'spr17')
        self.assertEqual('(T, R)', c.days_str())