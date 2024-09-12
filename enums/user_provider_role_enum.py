from enum import Enum

# UserProviderRoleEnum with ranking
class UserProviderRoleEnum(str, Enum):
    OWNER = ("Owner", 1)
    MODERATOR = ("Moderator", 2)

    def __new__(cls, value, rank):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.rank = rank
        return obj

    def __lt__(self, other):
        if isinstance(other, UserProviderRoleEnum):
            return self.rank < other.rank
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, UserProviderRoleEnum):
            return self.rank > other.rank
