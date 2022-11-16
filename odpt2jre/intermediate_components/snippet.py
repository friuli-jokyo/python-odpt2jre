from __future__ import annotations

from enum import Enum, auto

from odpt2jre.intermediate_components.station import BetweenStations, SingleStation


class SnippetEnum(Enum):
    """
    Enumerates the IDs of snippets.
    """

    NULL = auto()
    STAFF_IS_ON_THE_WAY = auto()
    NOT_STOP_AT_STATION = auto()
    MAY_TAKE_LONGER_TIME = auto()
    STOP_AT_EACH_STATION = auto()
    SPECIAL_RAPID_NOT_STOP = auto()
    NUMBER_OF_TRAINS_REDUCED = auto()
    WOMEN_ONLY_CAR_DISCONTINUED = auto()

class Snippet:

    enum: SnippetEnum = SnippetEnum.NULL
    stations: list[SingleStation]
    sections: list[BetweenStations]

    def __init__(self, enum:SnippetEnum) -> None:
        self.enum = enum
        self.stations = []
        self.sections = []

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
            case SnippetEnum.SPECIAL_RAPID_NOT_STOP:
                return "特別快速・青梅特快は停車しません。"
            case SnippetEnum.NUMBER_OF_TRAINS_REDUCED:
                return "運転本数が少なくなっています。"
            case SnippetEnum.WOMEN_ONLY_CAR_DISCONTINUED:
                return "女性専用車を中止しています。"
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
            case SnippetEnum.STOP_AT_EACH_STATION:
                if self.sections:
                    return "The line will stop at each station " + self.sections[0].format_en(use_lowercase=True) + "."
                else:
                    return "The line will stop at each station."
            case SnippetEnum.SPECIAL_RAPID_NOT_STOP:
                return "Special Rapid/Ōme Special Rapid does not stop."
            case SnippetEnum.NUMBER_OF_TRAINS_REDUCED:
                return "The number of trains running is currently reduced."
            case SnippetEnum.WOMEN_ONLY_CAR_DISCONTINUED:
                return "Women-only cars have been discontinued."
            case _:
                return ""

    def build_ko(self):
        match self.enum:
            case SnippetEnum.NULL:
                return ""
            case SnippetEnum.STAFF_IS_ON_THE_WAY:
                return "역무원이 현장으로 향하고 있습니다."
            case SnippetEnum.NOT_STOP_AT_STATION:
                if self.stations:
                    return "" #TODO
                else:
                    return ""
            case SnippetEnum.MAY_TAKE_LONGER_TIME:
                return "목적지까지 평소보다 시간을 많이 소요하는 경우가 있습니다."
            case SnippetEnum.STOP_AT_EACH_STATION:
                if self.sections:
                    return "" #TODO
                else:
                    return "" #TODO
            case SnippetEnum.SPECIAL_RAPID_NOT_STOP:
                return "특별 쾌속오메 특별쾌속은 정차하지 않아요."
            case SnippetEnum.NUMBER_OF_TRAINS_REDUCED:
                return "운행 열차수가 적어지고 있습니다."
            case SnippetEnum.WOMEN_ONLY_CAR_DISCONTINUED:
                return "여성 전용 차량을 중지합니다."
            case _:
                return ""

    def build_zh_CN(self):
        match self.enum:
            case SnippetEnum.NULL:
                return ""
            case SnippetEnum.STAFF_IS_ON_THE_WAY:
                return "工作人员正在前往现场。"
            case SnippetEnum.NOT_STOP_AT_STATION:
                if self.stations:
                    return "" #TODO
                else:
                    return ""
            case SnippetEnum.MAY_TAKE_LONGER_TIME:
                return "可能需要比以往更长的时间到达目的地。"
            case SnippetEnum.STOP_AT_EACH_STATION:
                if self.sections:
                    return "" #TODO
                else:
                    return "" #TODO
            case SnippetEnum.SPECIAL_RAPID_NOT_STOP:
                return "特别快、青梅特快不会停车。"
            case SnippetEnum.NUMBER_OF_TRAINS_REDUCED:
                return "运行班次已减少。"
            case SnippetEnum.WOMEN_ONLY_CAR_DISCONTINUED:
                return "我们正在停止女性专用车。"
            case _:
                return ""

    def build_zh_TW(self):
        match self.enum:
            case SnippetEnum.NULL:
                return ""
            case SnippetEnum.STAFF_IS_ON_THE_WAY:
                return "工作人員正在前往現場。"
            case SnippetEnum.NOT_STOP_AT_STATION:
                if self.stations:
                    return "" #TODO
                else:
                    return ""
            case SnippetEnum.MAY_TAKE_LONGER_TIME:
                return "可能需要比以往更長的時間到達目的地。"
            case SnippetEnum.STOP_AT_EACH_STATION:
                if self.sections:
                    return "" #TODO
                else:
                    return "" #TODO
            case SnippetEnum.SPECIAL_RAPID_NOT_STOP:
                return "特別快、青梅特快不會停車。"
            case SnippetEnum.NUMBER_OF_TRAINS_REDUCED:
                return "運行班次已減少。"
            case SnippetEnum.WOMEN_ONLY_CAR_DISCONTINUED:
                return "我們將停止女性專用車。"
            case _:
                return ""
