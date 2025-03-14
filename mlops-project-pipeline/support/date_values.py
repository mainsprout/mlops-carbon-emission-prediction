from enum import Enum
from pytz import timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class DateFormat(Enum):
    yyyyMMddHHmmss = "%Y%m%d%H%M%S"
    yyyyMMddHHmm = "%Y%m%d%H%M"
    yyyyMMdd = "%Y%m%d"
    yyyyMM = "%Y%m"
    formattedYyyyMMddHHmmss = "%Y-%m-%d %H:%M:%S"


class DateValues:

    @staticmethod
    def get_current_date():
        """
        Return current date in yyyyMMdd format

        :returns: current date
        :rtype: str
        """
        return datetime.now(timezone('Asia/Seoul')).strftime(DateFormat.yyyyMMdd.value)

    @staticmethod
    def get_before_60_days():
        """
        Return date of 60 days before the current date in yyyyMMdd format

        :returns: date of 60 days before
        :rtype: str
        """
        return (datetime.now(timezone('Asia/Seoul')) - relativedelta(days=60)).strftime(DateFormat.yyyyMMdd.value)

    @staticmethod
    def get_before_one_day(base_day: str = None) -> str:
        """
        Return the date of one day before the given base date or the current date in yyyyMMdd format.

        :param str base_day: Base date in yyyyMMdd format (optional)
        :returns: Date of one day before the given base date or current date in yyyyMMdd format
        :rtype: str
        """
        # Check if base_day is provided
        if base_day:
            try:
                base_date = datetime.strptime(base_day, "%Y%m%d")
            except ValueError:
                raise ValueError("base_day must be in yyyyMMdd format.")
        else:
            # Get current time in 'Asia/Seoul' timezone
            base_date = datetime.now(timezone('Asia/Seoul'))

        # Subtract one day
        one_day_before = base_date - timedelta(days=1)

        # Return the formatted date
        return one_day_before.strftime("%Y%m%d")

    @staticmethod
    def get_before_one_month(base_day: str = None):
        """
        Return date of 1 month before the base date (or current date if not provided)

        :param str base_day: Base date in yyyyMM or yyyyMMdd format
        :returns: date of 1 month before the base date
        :rtype: str
        """
        if base_day:
            month_len = 6
            day_len = 8
            if len(base_day) not in [month_len, day_len]:
                raise ValueError("Length of base_day is not allowed.")
            return (datetime.strptime((base_day[:6] + "01"), DateFormat.yyyyMMdd.value) - relativedelta(
                months=1)).strftime(DateFormat.yyyyMM.value)
        return (datetime.now(timezone('Asia/Seoul')) - relativedelta(months=1)).strftime(DateFormat.yyyyMM.value)


    @staticmethod
    def get_previous_week(base_day: str = None) -> str:
        """
        Return the date of one week ago from the given base day in yyyyMMdd format.

        :param str base_day: Base date in yyyyMMdd format (optional)
        :returns: Date of one week ago in yyyyMMdd format
        :rtype: str
        """
        if base_day:
            try:
                base_date = datetime.strptime(base_day, "%Y%m%d")
            except ValueError:
                raise ValueError("base_day must be in yyyyMMdd format.")
        else:
            base_date = datetime.now(timezone('Asia/Seoul'))

        # Calculate one week ago
        one_week_ago = base_date - timedelta(days=7)

        # Return the formatted date
        return one_week_ago.strftime("%Y%m%d")

    @staticmethod
    def get_datetime_list(start_day, end_day):
        """
        Return a list of datetime strings (yyyyMMddHHmm) between start_day and end_day

        :param str start_day: Start date with time (format: yyyyMMddHHmm)
        :param str end_day: End date with time (format: yyyyMMddHHmm)
        :returns: list of date strings (e.g. ['202401111100', '202401111110', ...])
        :rtype: List

        >>> from support.date_values import DateValues
        >>> date_value = DateValues()
        >>> result = date_value.get_datetime_list('202401111100', '202401111130')
        >>> result
        ['202401111100', '202401111110', '202401111120', '202401111130']
        """
        datetime_list = []
        try:
            start_datetime = datetime.strptime(start_day, DateFormat.yyyyMMddHHmm.value)
            end_datetime = datetime.strptime(end_day, DateFormat.yyyyMMddHHmm.value)
            while start_datetime <= end_datetime:
                datetime_list.append(start_datetime.strftime(DateFormat.yyyyMMddHHmm.value))
                start_datetime += timedelta(minutes=10)  # Adjust the interval if needed
            return datetime_list
        except ValueError:
            raise ValueError("You have entered a date in an incorrect format. "
                             f"Please double-check the date: start_day = {start_day}, end_day = {end_day}")
