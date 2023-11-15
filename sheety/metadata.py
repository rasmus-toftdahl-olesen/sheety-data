from collections import namedtuple
from datetime import datetime
from typing import ClassVar, Dict

import gspread

Locale = namedtuple(typename="Locale", field_names=("locale", "to_str", "from_str"))


DA_DK_FORMAT = "%d/%m/%Y %H.%M.%S"


def da_dk_to_str(dt: datetime) -> str:
    return format(dt, DA_DK_FORMAT)


def da_dk_from_str(s: str) -> datetime:
    return datetime.strptime(s, DA_DK_FORMAT)


class Metadata:
    PRODUCT: ClassVar[str] = "Sheety Data"
    VERSION: ClassVar[int] = 1
    LOCALES: ClassVar[Dict[str, Locale]] = {
        "da_DK": Locale("da_DK", da_dk_to_str, da_dk_from_str),
    }

    sheet: gspread.Worksheet
    version: int
    expected_type: str
    actual_type: str
    locale: Locale

    def __init__(self, sheet: gspread.Worksheet, expected_type: str):
        self.sheet = sheet
        self.version = -1
        self.expected_type = expected_type
        self.actual_type = f"???UNKNOWN {Metadata.PRODUCT} type???"
        self._validate()

    def add_metadata(self):
        self.sheet.update(
            range_name="A1:C1",
            values=[[Metadata.PRODUCT, Metadata.VERSION, self.expected_type]],
        )

    def datetime_from_str(self, s: str) -> datetime:
        return self.locale.from_str(s)

    def datetime_to_str(self, dt: datetime) -> datetime:
        return self.locale.to_str(dt)

    def _validate(self):
        # values = self.sheet.get_values('A1:C2')
        row1_values = self.sheet.row_values(1)
        empty_sheet = len(row1_values) == 0
        # empty_sheet = self.sheet.column_count == 0 and self.sheet.row_count == 0
        if empty_sheet:
            self.add_metadata()
            self._validate()
        else:
            assert len(row1_values) >= 3
            product, version, type_ = row1_values[:3]
            version = int(version)
            assert (
                product == Metadata.PRODUCT
            ), f'Cell A1 expected to be "{Metadata.PRODUCT}" but was "{product}"'
            assert (
                version == Metadata.VERSION
            ), f'Cell B1 expected to be "{Metadata.VERSION}" but was "{version}"'
            assert (
                type_ == self.expected_type
            ), f'Cell C1 expected to be "{self.expected_type}" but was "{type_}"'
            self.actual_type = type_

            locale = self.sheet.spreadsheet.locale
            assert (
                locale in Metadata.LOCALES
            ), f'Unknown locale in spreadsheet "{locale}, current only these locales are supported: {Metadata.LOCALES.keys()}"'
            self.locale = Metadata.LOCALES[locale]
