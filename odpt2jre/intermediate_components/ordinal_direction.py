from enum import Enum

class OrdinalDirection(Enum):
    """
    Enumerates the IDs of ordinal direction.
    """
    NORTH = "北"
    SOUTH = "南"
    EAST = "東"
    WEST = "西"

    def format_ja(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"北"``
        """
        return self.value
