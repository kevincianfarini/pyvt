from unittest import TestCase
from api.travis import Travis


class TestFoo(TestCase):

    def test_foo(self):
        self.assertEquals(1, Travis.travis_foo())
