from __future__ import annotations

from odpt2jre.intermediate_components.station import SingleStation

from .enums import StringEnum, auto


class SnippetEnum(StringEnum):
    """
    Enumerates the IDs of snippets.
    """

    NULL = auto()
    STAFF_IS_ON_THE_WAY = auto()
    NOT_STOP_AT_STATION = auto()
    MAY_TAKE_LONGER_TIME = auto()

class Snippet:

    enum: SnippetEnum = SnippetEnum.NULL
    stations: list[SingleStation]

    def __init__(self, enum:SnippetEnum) -> None:
        self.enum = enum
        self.stations = []

    def __bool__(self) -> bool:
        if self.enum == SnippetEnum.NULL:
            return False
        else:
            return True

    def build_ja(self):
        match self.enum:
            case SnippetEnum.NULL:
                return ""
            case SnippetEnum.STAFF_IS_ON_THE_WAY:
                return "係員が現地に向かっています。"
            case SnippetEnum.NOT_STOP_AT_STATION:
                if self.stations:
                    return "・".join([ station.format_ja() for station in self.stations ]) + "には停車しません。"
                else:
                    return ""
            case SnippetEnum.MAY_TAKE_LONGER_TIME:
                return "目的地まで通常より大幅に時間を要する場合があります。"
            case _:
                return ""

    def build_en(self):
        match self.enum:
            case SnippetEnum.NULL:
                return ""
            case SnippetEnum.STAFF_IS_ON_THE_WAY:
                return "A staff member is on the way to the spot."
            case SnippetEnum.NOT_STOP_AT_STATION:
                if self.stations:
                    return "The line will not stop at " + " and ".join([ station.format_en() for station in self.stations ]).replace(" Station","") + " station."
                else:
                    return ""
            case SnippetEnum.MAY_TAKE_LONGER_TIME:
                return "It may take much longer than usual to reach your destination."
            case _:
                return ""
