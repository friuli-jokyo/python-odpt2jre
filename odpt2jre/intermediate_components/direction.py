import re
from typing import Optional
from enum import Enum

from .output_dict import MultiLanguageDictWithId
from .multi_language_expression import MultiLanguageExpression
from .station import StationName


class DirectionEnum(Enum):

    NULL = "null"
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    INBOUND_AND_OUTBOUND = "inbound_and_outbound"
    INNER_CIRCLE = "inner_circle"
    OUTER_CIRCLE = "outer_circle"
    INNER_AND_OUTER_CIRCLE = "inner_and_outer_circle"
    FOR_STATION = "for_station"

    def is_circle(self) -> bool:
        match self:
            case DirectionEnum.INNER_AND_OUTER_CIRCLE:
                return True
            case DirectionEnum.INNER_CIRCLE:
                return True
            case DirectionEnum.OUTER_CIRCLE:
                return True
            case _:
                return False

    def format_ja(self) -> str:
        match self:
            case DirectionEnum.NULL:
                return ""
            case DirectionEnum.INBOUND:
                return "上り線"
            case DirectionEnum.OUTBOUND:
                return "下り線"
            case DirectionEnum.INBOUND_AND_OUTBOUND:
                return "上下線"
            case DirectionEnum.INNER_CIRCLE:
                return "内回り"
            case DirectionEnum.OUTER_CIRCLE:
                return "外回り"
            case DirectionEnum.INNER_AND_OUTER_CIRCLE:
                return "内・外回り"
            case DirectionEnum.FOR_STATION:
                return "方面"
            case _:
                raise ValueError

    def format_en(self) -> str:
        match self:
            case DirectionEnum.NULL:
                return ""
            case DirectionEnum.INBOUND:
                return "Inbound line"
            case DirectionEnum.OUTBOUND:
                return "Outbound line"
            case DirectionEnum.INBOUND_AND_OUTBOUND:
                return "Inbound and outbound lines"
            case DirectionEnum.INNER_CIRCLE:
                return "Inner circle"
            case DirectionEnum.OUTER_CIRCLE:
                return "Outer circle"
            case DirectionEnum.INNER_AND_OUTER_CIRCLE:
                return "Inner,Outer circle"
            case DirectionEnum.FOR_STATION:
                return "For"
            case _:
                raise ValueError

    def format_ko(self) -> str:
        match self:
            case DirectionEnum.NULL:
                return ""
            case DirectionEnum.INBOUND:
                return "상행선"
            case DirectionEnum.OUTBOUND:
                return "하행선"
            case DirectionEnum.INBOUND_AND_OUTBOUND:
                return "상하행선"
            case DirectionEnum.INNER_CIRCLE:
                return "내선 순환"
            case DirectionEnum.OUTER_CIRCLE:
                return "외선 순환"
            case DirectionEnum.INNER_AND_OUTER_CIRCLE:
                return "외,내선 순환"
            case DirectionEnum.FOR_STATION:
                return "방면"
            case _:
                raise ValueError

    def format_zh_CN(self) -> str:
        match self:
            case DirectionEnum.NULL:
                return ""
            case DirectionEnum.INBOUND:
                return "上行线"
            case DirectionEnum.OUTBOUND:
                return "下行线"
            case DirectionEnum.INBOUND_AND_OUTBOUND:
                return "上下行线"
            case DirectionEnum.INNER_CIRCLE:
                return "内环"
            case DirectionEnum.OUTER_CIRCLE:
                return "外环"
            case DirectionEnum.INNER_AND_OUTER_CIRCLE:
                return "内、外环"
            case DirectionEnum.FOR_STATION:
                return "方向"
            case _:
                raise ValueError

    def format_zh_TW(self) -> str:
        match self:
            case DirectionEnum.NULL:
                return ""
            case DirectionEnum.INBOUND:
                return "上行線"
            case DirectionEnum.OUTBOUND:
                return "下行線"
            case DirectionEnum.INBOUND_AND_OUTBOUND:
                return "上下行線"
            case DirectionEnum.INNER_CIRCLE:
                return "內環"
            case DirectionEnum.OUTER_CIRCLE:
                return "外環"
            case DirectionEnum.INNER_AND_OUTER_CIRCLE:
                return "內、外環"
            case DirectionEnum.FOR_STATION:
                return "方向"
            case _:
                raise ValueError

    @classmethod
    def embed_field(cls, text:str) -> str:
        for enum in sorted(cls, reverse=True, key= lambda x: len(x.format_ja())):
            if enum == DirectionEnum.NULL:
                continue
            if enum == DirectionEnum.FOR_STATION:
                continue
            field = f"[Direction:{enum.value}]"
            text = text.replace(enum.format_ja(),field)
        return text

class Direction(MultiLanguageExpression, header="Direction"):

    enum: DirectionEnum = DirectionEnum.NULL
    _station: Optional[StationName] = None

    def __init__(self, field: str) -> None:
        super().__init__(field)
        if len(self._args)==1:
            if re.fullmatch( StationName.regex, self._args[0] ):
                self.enum = DirectionEnum.FOR_STATION
                self._station = StationName(self._args[0])
            else:
                self.enum = DirectionEnum(self._args[0])
        else:
            raise ValueError("Invalid argument number.")

    def is_circle(self) -> bool:
        return self.enum.is_circle()

    def format_ja(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"上り線"``, ``"東京方面"``
        """
        match self.enum:
            case DirectionEnum.NULL:
                return ""
            case DirectionEnum.FOR_STATION:
                if self._station:
                    return self._station.format_ja()+self.enum.format_ja()
                else:
                    return ""
            case _:
                return self.enum.format_ja()

    def format_en(self, in_sentence:bool = False) -> str:
        """
        Returns
        -------
        str
            e.g. ``"Inbound line"``, ``"For Tōkyō"``
        """
        match self.enum:
            case DirectionEnum.NULL:
                return ""
            case DirectionEnum.FOR_STATION:
                if self._station:
                    if in_sentence:
                        return "bound for "+self._station.format_en()
                    else:
                        return self.enum.format_en()+" "+self._station.format_en()
                else:
                    return ""
            case _:
                return self.enum.format_en()

    def format_ko(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"상행선"``, ``"도쿄방면"``
        """
        match self.enum:
            case DirectionEnum.NULL:
                return ""
            case DirectionEnum.FOR_STATION:
                if self._station:
                    return self._station.format_ko()+self.enum.format_ko()
                else:
                    return ""
            case _:
                return self.enum.format_ko()

    def format_zh_CN(self, in_sentence:bool = False) -> str:
        """
        Returns
        -------
        str
            e.g. ``"上行线"``, ``"东京方向"``
        """
        match self.enum:
            case DirectionEnum.NULL:
                return ""
            case DirectionEnum.FOR_STATION:
                if self._station:
                    if in_sentence:
                        return self._station.format_zh_CN()+"方面"
                    else:
                        return self._station.format_zh_CN()+self.enum.format_zh_CN()
                else:
                    return ""
            case _:
                return self.enum.format_zh_CN()

    def format_zh_TW(self, in_sentence:bool = False) -> str:
        """
        Returns
        -------
        str
            e.g. ``"上行線"``, ``"東京方向"``
        """
        match self.enum:
            case DirectionEnum.NULL:
                return ""
            case DirectionEnum.FOR_STATION:
                if self._station:
                    if in_sentence:
                        return self._station.format_zh_TW()+"方面"
                    else:
                        return self._station.format_zh_TW()+self.enum.format_zh_TW()
                else:
                    return ""
            case _:
                return self.enum.format_zh_TW()

    def to_dict(self) -> MultiLanguageDictWithId:
        result:MultiLanguageDictWithId = {
            "id": self.enum.name,
            "ja": self.format_ja(),
            "en": self.format_en(),
            "ko": self.format_ko(),
            "zh-Hans": self.format_zh_CN(),
            "zh-Hant": self.format_zh_TW(),
        }
        # result["ja-Hrkt"] = self.
        return result
