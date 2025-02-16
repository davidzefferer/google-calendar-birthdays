from dataclasses import dataclass

from datetime import datetime

@dataclass
class Birthday:
    name: str
    contact: str
    year: int
    month: int
    day: int

    def as_date(self) -> datetime:
        year = self.year
        if year is None:
            # Year is unkown; use the current year
            year = datetime.now().year
        return datetime(year, self.month, self.day)
