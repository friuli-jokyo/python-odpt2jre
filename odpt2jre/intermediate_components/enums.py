from enum import Enum, auto

__all__ = ["StringEnum","auto"]

class StringEnum(Enum):

    @classmethod
    def from_str(cls, st: str):
        for one in cls:
            if one.name == st:
                return one
        raise ValueError
