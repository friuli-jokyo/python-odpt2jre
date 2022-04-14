from typing import Optional

from .common import concat_ja
from .direction import Direction, DirectionEnum
from .line import LineName
from .multi_language_expression import MultiLanguageExpression
from .station import BetweenStations, OrdinalDirectionFromStaton


class StatusModifier:

    still: bool = False
    lines: list[LineName]
    sections: list[BetweenStations|OrdinalDirectionFromStaton]
    direction: Optional[Direction] = None
    some_train: bool = False
    others: list[str]
    """
    ja: "快速運転","女性専用車", etc.
    """

    def __init__(self) -> None:
        self.lines = []
        self.sections = []
        self.others = []

    def __bool__(self) -> bool:
        if self.still:
            return True
        if self.lines:
            return True
        if self.sections:
            return True
        if self.direction:
            return True
        if self.some_train:
            return True
        if self.others:
            return True
        return False

    def append_content(self, obj:MultiLanguageExpression) -> None:
        match obj:
            case LineName():
                self.lines += [obj]
            case BetweenStations() | OrdinalDirectionFromStaton():
                self.sections += [obj]
            case _:
                pass

    def build_place_ja(self, postfix: str = "") -> str:
        result: list[str] = []
        if self.sections:
            section_count = len(self.sections)
            for i, section in enumerate(self.sections):
                result.append(section.format_ja())
                if i<section_count-1: # is not last of loop
                    match section:
                        case BetweenStations():
                            result.append("・")
                        case OrdinalDirectionFromStaton():
                            result.append("、")

        if result:
            result.append(postfix)

        return "".join(result)

    def build_ja(self, postfix: str = "", exclude_some_train: bool = False):

        original_some_train = self.some_train
        if exclude_some_train:
            self.some_train = False
        result: list[str] = []
        if self.still:
            still = "現在も"
        else:
            still = ""
        if place := self.build_place_ja():
            result.append(place)
        if self.direction:
            if self.direction.enum == DirectionEnum.FOR_STATION:
                if self.some_train:
                    result.append(self.direction.format_ja()+"行き一部列車")
                else:
                    result.append(self.direction.format_ja()+"行き列車")
            elif self.direction.is_circle():
                if self.some_train:
                    result.append("一部")
                result.append(self.direction.format_ja()+"電車")
            else:
                result.append(self.direction.format_ja())
                if self.some_train:
                    result.append("一部列車")
        else:
            if self.some_train:
                result.append("一部列車")

        if self.others:
            result.append(concat_ja(self.others))

        self.some_train = original_some_train

        if result:
            return "の".join(result)+postfix
        else:
            return still

    def build_main_en(self, section_preposition:str, some_at_first:bool = False ) -> tuple[list[str], list[str], list[str]]:

        pre_line: list[str] = []
        post_line: list[str] = []
        post_status: list[str] = []

        if len(self.sections) > 0:
            section = self.sections[0]
        else:
            section = None

        # Before line name
        if self.some_train and some_at_first:
            pre_line.append("Some of the trains on")

        # After line name
        if self.direction:
            post_line.append(self.direction.format_en())
        else:
            post_line.append(DirectionEnum.INBOUND_AND_OUTBOUND.format_en())

        if section and section_preposition:
            match section:
                case BetweenStations():
                    post_line.append(section_preposition)
                    post_line.append(section.format_en())
                case _:
                    pass

        # After status
        if self.some_train and not some_at_first:
            post_status.append("on some trains")

        return pre_line, post_line, post_status
