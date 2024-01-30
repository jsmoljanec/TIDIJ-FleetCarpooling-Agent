import unittest

from UDP.entities.utilities.date_time_utils import DateTimeUtils


class DateTimeUtilsTest(unittest.TestCase):
    def test_is_current_time_between_dates__string_given_dates_with_valid_dates_returns_true(self):
        date_time_format = "%Y-%m-%d %H:%M"
        pickup_datetime = "2024-01-24 12:00"
        return_datetime = "2026-01-24 12:00"
        check = DateTimeUtils().is_current_time_between_dates__string(pickup_datetime, return_datetime,
                                                                      date_time_format)
        self.assertEqual(check, True)

    def test_is_current_time_between_dates__string_given_dates_with_invalid_dates_returns_false(self):
        date_time_format = "%Y-%m-%d %H:%M"
        pickup_datetime = "2021-01-24 12:00"
        return_datetime = "2022-01-24 12:00"
        check = DateTimeUtils().is_current_time_between_dates__string(pickup_datetime, return_datetime,
                                                                      date_time_format)
        self.assertEqual(check, False)
