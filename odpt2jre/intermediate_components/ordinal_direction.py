from .enums import StringEnum, auto

class OrdinalDirection(StringEnum):
    """
    Enumerates the IDs of ordinal direction.
    """
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

    def format_ja(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"北"``
        """
        match self:
            case self.NORTH:
                return "北"
            case self.SOUTH:
                return "南"
            case self.EAST:
                return "東"
            case self.WEST:
                return "西"
            case _:
                raise ValueError

    @classmethod
    def from_ja(cls, st:str):
        match st:
            case "北":
                return OrdinalDirection.NORTH
            case "南":
                return OrdinalDirection.SOUTH
            case "東":
                return OrdinalDirection.EAST
            case "西":
                return OrdinalDirection.WEST
            case _:
                raise ValueError("Invalid ordinal direction name.")