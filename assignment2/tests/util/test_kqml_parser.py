from unittest import TestCase

from util.kqml_parser import KQMLParser


class TestKQMLParser(TestCase):
    def setUp(self):
        self.parser = KQMLParser()

    def test_get_action(self):
        message = "(ask: (record-exists ?sample [1,2,3]))"
        action = self.parser.get_action(message)

        self.assertEqual("ask", action)

    def test_get_condition(self):
        message = "(ask: (record-exists ?sample [1,2,3]))"
        condition = self.parser.get_condition(message)

        self.assertEqual("record-exists", condition)

    def test_get_criteria(self):
        message = "(ask: (record-exists ?sample [1,2,3]))"
        criteria = self.parser.get_criteria(message)

        self.assertEqual("?sample", criteria)

    def test_get_comparer(self):
        message = "(ask: (record-exists ?sample [1,2,3]))"
        comparer = self.parser.get_comparer(message, "sample")

        self.assertEqual("[1,2,3]", comparer)
