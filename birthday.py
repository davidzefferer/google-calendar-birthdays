from dataclasses import dataclass

from datetime import datetime


@dataclass
class Birthday:
    name: str
    year: int
    month: int
    day: int
    contact: str
    event_id: str

    def as_date(self) -> datetime:
        year = self.year
        if year is None:
            # Year is unkown; use the current year
            year = datetime.now().year
            if self.month == 2 and self.day == 29:
                # year must be a leap year
                year = Birthday.__get_last_leap_year__(year)

        return datetime(year, self.month, self.day)

    def __get_last_leap_year__(year: int):
        while not (
            (year % 4 == 0 and year % 100 != 0) or (year % 100 == 0 and year % 400 == 0)
        ):
            year -= 1
        return year

    def is_considered_same_birthday(self, other: "Birthday") -> bool:
        return (
            self.name == other.name
            and self.month == other.month
            and self.day == other.day
        )
