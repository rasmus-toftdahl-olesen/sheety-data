import gspread
import pytest

from sheety.metadata import Metadata


def test_empty_sheet(mocker):
    sheet = mocker.Mock(gspread.Worksheet)
    sheet.column_count = 0
    sheet.row_count = 0

    mocked_update = None

    def update_mock(range_name, values):
        global mocked_update
        mocked_update = values
        sheet.column_count = 3
        sheet.row_count = 1

    def row_values_mock(row):
        global mocked_update

        return mocked_update

    sheet.update = update_mock
    sheet.row_values = row_values_mock
    metadata = Metadata(sheet, expected_type="My data type")


def test_already_existing_sheet(mocker):
    sheet = mocker.Mock(gspread.Worksheet)
    sheet.column_count = 10
    sheet.row_count = 10
    sheet.row_values = lambda row: (Metadata.PRODUCT, Metadata.VERSION, "My data type")
    metadata = Metadata(sheet, expected_type="My data type")
    assert metadata.type == "My data type"


def test_bad_product(mocker):
    sheet = mocker.Mock(gspread.Worksheet)
    sheet.column_count = 10
    sheet.row_count = 10
    sheet.row_values = lambda row: ("Wrong prouduct", Metadata.VERSION, "My data type")
    with pytest.raises(AssertionError):
        Metadata(sheet, expected_type="My data type")


def test_bad_version(mocker):
    sheet = mocker.Mock(gspread.Worksheet)
    sheet.column_count = 10
    sheet.row_count = 10
    sheet.row_values = lambda row: (Metadata.PRODUCT, -42, "c")
    with pytest.raises(AssertionError):
        Metadata(sheet, expected_type="My data type")


def test_bad_type(mocker):
    sheet = mocker.Mock(gspread.Worksheet)
    sheet.column_count = 10
    sheet.row_count = 10
    sheet.row_values = lambda row: (
        Metadata.PRODUCT,
        Metadata.VERSION,
        "WRONG DATA TYPE",
    )
    with pytest.raises(AssertionError):
        Metadata(sheet, expected_type="My data type")
