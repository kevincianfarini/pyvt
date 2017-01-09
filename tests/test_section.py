from unittest import TestCase
from pyvt.section import Section


class TestClass(TestCase):

    def test_init(self):
        s = Section(dummy='dummy')
        self.assertIsNotNone(s)
        self.assertIsNotNone(getattr(s, 'dummy'))

    def test_tuple_str(self):
        tup = ('this', 'is', 'a', 'test')
        self.assertNotIn("'", Section.tuple_str(tup))

    def test_str_rep(self):
        data = {'name': 'STAT 4705', 'crn': '17583', 'days': 'TR',
                'start_time': '9:30AM', 'end_time': '10:45AM'}
        self.assertEqual('STAT 4705 (17583) on TR at (9:30AM, 10:45AM)', str(Section(**data)))

    def test_eq_true(self):
        self.assertNotEquals(10, Section()) #not same type
        self.assertEqual(Section(dummy='dummy'), Section(dummy='dummy'))
        self.assertNotEquals(Section(), Section(dummy='dummy'))