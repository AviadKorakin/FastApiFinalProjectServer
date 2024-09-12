from enum import Enum

class DayOfWeekEnum(str, Enum):
    SUNDAY = ("Sunday", 1)
    MONDAY = ("Monday", 2)
    TUESDAY = ("Tuesday", 3)
    WEDNESDAY = ("Wednesday", 4)
    THURSDAY = ("Thursday", 5)
    FRIDAY = ("Friday", 6)
    SATURDAY = ("Saturday", 7)

    def __new__(cls, value, rank):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.rank = rank
        return obj

    def __lt__(self, other):
        if isinstance(other, DayOfWeekEnum):
            return self.rank < other.rank
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, DayOfWeekEnum):
            return self.rank > other.rank
        return NotImplemented
