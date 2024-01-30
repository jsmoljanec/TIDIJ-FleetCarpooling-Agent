import unittest

from UDP.entities.utilities.strings import Strings


class StringsTest(unittest.TestCase):
    def test_displaying_right_written_strings(self):
        self.assertEqual(Strings.START_COMMAND, "start")
        self.assertEqual(Strings.STOP_COMMAND, "stop")
        self.assertEqual(Strings.RESTART_COMMAND, "restart")
        self.assertEqual(Strings.CURRENT_POSITION_COMMAND, "current-position")

    def test_displaying_misspelled_strings(self):
        self.assertNotEqual(Strings.CURRENT_POSITION_COMMAND, "current position")
