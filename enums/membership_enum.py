from enum import Enum

class MembershipEnum(str, Enum):
    FREE = ("Free", 2)
    PREMIUM = ("Premium", 1)

    def __new__(cls, value, rank):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.rank = rank
        return obj

    def __lt__(self, other):
        if isinstance(other, MembershipEnum):
            return self.rank < other.rank
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, MembershipEnum):
            return self.rank > other.rank
        return NotImplemented

