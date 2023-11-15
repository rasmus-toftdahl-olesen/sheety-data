from datetime import timedelta, datetime

import gspread
import gspread.utils

from sheety.metadata import Metadata


class Timeseries:
    TYPE = "TimeSeries"

    def __init__(self, sheet: gspread.Worksheet, interval: timedelta):
        self.metadata = Metadata(sheet, Timeseries.TYPE)
        self.interval = interval
        self.first_time = None
        # self.metadata.sheet.format("A2:A10", {"numberFormat": "DATE_TIME"})
        if self.metadata.sheet.row_count > 1:
            a2 = self.metadata.sheet.get("A2")
            if a2:
                self.first_time = self.metadata.datetime_from_str(a2.first())

    def update(self, value, now: datetime = None):
        if now is None:
            now = datetime.now()
        if self.first_time is None:
            index = 2
        else:
            assert (
                now > self.first_time
            ), f'The datetime of the first cell (A2) "{self.first_time}" is larger than the current date "{now}".'
            diff = now - self.first_time
            index = 2 + int(diff / self.interval)
        range_name = f"A{index}:B{index}"
        now_as_str = self.metadata.datetime_to_str(now)
        # self.metadata.sheet.format(
        #     f"A{index}",
        #     {
        #         "numberFormat": {
        #             "type": "DATE_TIME",
        #             "pattern": self.metadata.locale.format,
        #         }
        #     },
        # )

        self.metadata.sheet.update(
            range_name=range_name,
            values=[[now_as_str, value]],
            value_input_option=gspread.utils.ValueInputOption.user_entered,
        )
