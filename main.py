# This is a sample Python script.
from datetime import timedelta

import gspread

from sheety.timeseries import Timeseries


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {name}")  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print_hi("PyCharm")

    gc = gspread.service_account()
    sheet = gc.open("Google Sheet Metrics - Example1").sheet1
    series = Timeseries(sheet, interval=timedelta(hours=1))
    series.update(42.42)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
