from datetime import datetime


class DateTimeUtils:
    @staticmethod
    def convert_date_time_from_string(date, time, date_time_format):
        return datetime.strptime(f"{date} {time}", date_time_format)

    @staticmethod
    def convert_date_time_to_number(date_time):
        return int((date_time - datetime(1970, 1, 1)).total_seconds() / 60)

    @staticmethod
    def is_current_time_between_dates__num(pickup_datetime, return_datetime):
        current_datetime = datetime.now()
        current_datetime_number = DateTimeUtils.convert_date_time_to_number(current_datetime)

        return pickup_datetime <= current_datetime_number <= return_datetime

    @staticmethod
    def is_current_time_between_dates__string(pickup_datetime, return_datetime):
        current_datetime = datetime.now()

        return pickup_datetime <= current_datetime <= return_datetime
