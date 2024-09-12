from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = ("ADMIN", 1)
    MODERATOR = ("MODERATOR", 2)
    USER = ("USER", 3)

    def __new__(cls, value, rank):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.rank = rank
        return obj

    def __lt__(self, other):
        if isinstance(other, RoleEnum):
            return self.rank < other.rank
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, RoleEnum):
            return self.rank > other.rank
        return NotImplemented
