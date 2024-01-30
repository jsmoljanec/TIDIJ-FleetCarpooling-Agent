import traceback
from datetime import datetime


class LoggingUtils:
    @staticmethod
    def log_exception():
        exception_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("exceptions.log", "a") as log_file:
            log_file.write(f"Exception occurred at: {exception_time}\n")
            traceback.print_exc(file=log_file)
