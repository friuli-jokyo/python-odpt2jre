from __future__ import annotations

from typing import Optional

from .common import concat_en, concat_ja
from .enums import StringEnum, auto
from .line import LineName
from .output_dict import MultiLanguageDictWithId
from .status_modifier import StatusModifier


class StatusEnum(StringEnum):
    """
    Enumerates the IDs of status.
    """

    NULL = auto()
    UNKNOWN = auto()
    NORMAL = auto()
    DELAY = auto()
    OPERATION_WILL_RESUME = auto()
    OPERATION_STOP = auto()
    OPERATION_RESUMED = auto()
    DESTINATION_CHANGE = auto()
    TURN_BACK_OPERATION = auto()
    DIRECT_STOP = auto()
    DIRECT_RESUMED = auto()
    STOP = auto()
    RESUMED = auto()
    CANCEL = auto()
    SOME_TRAIN_CANCEL = auto()
    SOME_SECTION_CANCEL = auto()
    ROUTE_CHANGE = auto()
    NOTICE = auto()

    def format_ja(self) -> str:
        match self:
            case StatusEnum.NULL:
                return ""
            case StatusEnum.UNKNOWN:
                return "状況不明"
            case StatusEnum.NORMAL:
                return "平常運転"
            case StatusEnum.DELAY:
                return "遅延"
            case StatusEnum.OPERATION_WILL_RESUME:
                return "運転再開見込"
            case StatusEnum.OPERATION_STOP:
                return "運転見合わせ"
            case StatusEnum.OPERATION_RESUMED:
                return "運転再開"
            case StatusEnum.DESTINATION_CHANGE:
                return ""
            case StatusEnum.TURN_BACK_OPERATION:
                return ""
            case StatusEnum.DIRECT_STOP:
                return "直通運転中止"
            case StatusEnum.DIRECT_RESUMED:
                return "直通運転再開"
            case StatusEnum.STOP:
                return ""
            case StatusEnum.RESUMED:
                return ""
            case StatusEnum.CANCEL:
                return "運休"
            case StatusEnum.SOME_TRAIN_CANCEL:
                return "一部運休"
            case StatusEnum.SOME_SECTION_CANCEL:
                return "一部運休"
            case StatusEnum.ROUTE_CHANGE:
                return "経路変更"
            case StatusEnum.NOTICE:
                return "お知らせ"
            case _:
                raise ValueError

    def format_en(self) -> str:
        match self:
            case StatusEnum.NULL:
                return ""
            case StatusEnum.UNKNOWN:
                return "{unknwon status}"
            case StatusEnum.NORMAL:
                return "Normal operation"
            case StatusEnum.DELAY:
                return "Delay"
            case StatusEnum.OPERATION_WILL_RESUME:
                return "Operation will resume"
            case StatusEnum.OPERATION_STOP:
                return "Operation suspended"
            case StatusEnum.OPERATION_RESUMED:
                return "Operation resumed"
            case StatusEnum.DESTINATION_CHANGE:
                return ""
            case StatusEnum.TURN_BACK_OPERATION:
                return ""
            case StatusEnum.DIRECT_STOP:
                return "Direct operation cancellation"
            case StatusEnum.DIRECT_RESUMED:
                return ""
            case StatusEnum.STOP:
                return ""
            case StatusEnum.RESUMED:
                return ""
            case StatusEnum.CANCEL:
                return ""
            case StatusEnum.SOME_TRAIN_CANCEL:
                return "Partial cancellation of service"
            case StatusEnum.SOME_SECTION_CANCEL:
                return "Partial cancellation of service"
            case StatusEnum.ROUTE_CHANGE:
                return "Route change"
            case StatusEnum.NOTICE:
                return "Notice"
            case _:
                raise ValueError

    def format_ko(self) -> str:
        match self:
            case StatusEnum.NULL:
                return ""
            case StatusEnum.UNKNOWN:
                return ""
            case StatusEnum.NORMAL:
                return "평상시 운행"
            case StatusEnum.DELAY:
                return "지연"
            case StatusEnum.OPERATION_WILL_RESUME:
                return "운행재개 예정"
            case StatusEnum.OPERATION_STOP:
                return "운행조정"
            case StatusEnum.OPERATION_RESUMED:
                return "운행재개"
            case StatusEnum.DESTINATION_CHANGE:
                return ""
            case StatusEnum.TURN_BACK_OPERATION:
                return ""
            case StatusEnum.DIRECT_STOP:
                return "직통운행 중지"
            case StatusEnum.DIRECT_RESUMED:
                return ""
            case StatusEnum.STOP:
                return ""
            case StatusEnum.RESUMED:
                return ""
            case StatusEnum.CANCEL:
                return ""
            case StatusEnum.SOME_TRAIN_CANCEL:
                return ""
            case StatusEnum.SOME_SECTION_CANCEL:
                return ""
            case StatusEnum.ROUTE_CHANGE:
                return "경로변경"
            case StatusEnum.NOTICE:
                return "알림"
            case _:
                raise ValueError

    def format_zh_CN(self) -> str:
        match self:
            case StatusEnum.NULL:
                return ""
            case StatusEnum.UNKNOWN:
                return ""
            case StatusEnum.NORMAL:
                return "正常运行"
            case StatusEnum.DELAY:
                return "晚点"
            case StatusEnum.OPERATION_WILL_RESUME:
                return "预计恢复运行"
            case StatusEnum.OPERATION_STOP:
                return "暂停运行"
            case StatusEnum.OPERATION_RESUMED:
                return "恢复运行"
            case StatusEnum.DESTINATION_CHANGE:
                return ""
            case StatusEnum.TURN_BACK_OPERATION:
                return ""
            case StatusEnum.DIRECT_STOP:
                return "停止直通运行"
            case StatusEnum.DIRECT_RESUMED:
                return ""
            case StatusEnum.STOP:
                return ""
            case StatusEnum.RESUMED:
                return ""
            case StatusEnum.CANCEL:
                return ""
            case StatusEnum.SOME_TRAIN_CANCEL:
                return ""
            case StatusEnum.SOME_SECTION_CANCEL:
                return ""
            case StatusEnum.ROUTE_CHANGE:
                return "线路变更"
            case StatusEnum.NOTICE:
                return "通知"
            case _:
                raise ValueError

    def format_zh_TW(self) -> str:
        match self:
            case StatusEnum.NULL:
                return ""
            case StatusEnum.UNKNOWN:
                return ""
            case StatusEnum.NORMAL:
                return "正常運行"
            case StatusEnum.DELAY:
                return "誤點"
            case StatusEnum.OPERATION_WILL_RESUME:
                return "運行再開預定"
            case StatusEnum.OPERATION_STOP:
                return "暫停運行"
            case StatusEnum.OPERATION_RESUMED:
                return "運行再開"
            case StatusEnum.DESTINATION_CHANGE:
                return ""
            case StatusEnum.TURN_BACK_OPERATION:
                return ""
            case StatusEnum.DIRECT_STOP:
                return "直通列車停止行駛"
            case StatusEnum.DIRECT_RESUMED:
                return ""
            case StatusEnum.STOP:
                return ""
            case StatusEnum.RESUMED:
                return ""
            case StatusEnum.CANCEL:
                return ""
            case StatusEnum.SOME_TRAIN_CANCEL:
                return ""
            case StatusEnum.SOME_SECTION_CANCEL:
                return ""
            case StatusEnum.ROUTE_CHANGE:
                return "線路變更"
            case StatusEnum.NOTICE:
                return "通知"
            case _:
                raise ValueError

    def get_icon(self) -> StatusIcon:
        match self:
            case StatusEnum.NORMAL:
                return StatusIcon.CIRCLE
            case StatusEnum.DELAY:
                return StatusIcon.TRIANGLE
            case StatusEnum.OPERATION_WILL_RESUME:
                return StatusIcon.NULL
            case StatusEnum.OPERATION_STOP:
                return StatusIcon.CROSS
            case StatusEnum.OPERATION_RESUMED:
                return StatusIcon.NULL
            case StatusEnum.DESTINATION_CHANGE:
                return StatusIcon.NULL
            case StatusEnum.TURN_BACK_OPERATION:
                return StatusIcon.NULL
            case StatusEnum.DIRECT_STOP:
                return StatusIcon.DIRECT_STOP
            case StatusEnum.DIRECT_RESUMED:
                return StatusIcon.NULL
            case StatusEnum.CANCEL:
                return StatusIcon.NULL
            case StatusEnum.SOME_TRAIN_CANCEL:
                return StatusIcon.TRIANGLE
            case StatusEnum.SOME_SECTION_CANCEL:
                return StatusIcon.TRIANGLE
            case StatusEnum.ROUTE_CHANGE:
                return StatusIcon.CIRCLE
            case StatusEnum.NOTICE:
                return StatusIcon.EXCLAMATION
            case _:
                return StatusIcon.QUESTION

    def get_prefix(self) -> str|None:
        match self:
            case StatusEnum.OPERATION_RESUMED|StatusEnum.OPERATION_STOP:
                return "OPERATION"
            case StatusEnum.DIRECT_RESUMED|StatusEnum.DIRECT_STOP:
                return "DIRECT"
            case _:
                return "NULL"

    def get_suffix(self) -> str|None:
        match self:
            case StatusEnum.OPERATION_STOP|StatusEnum.DIRECT_STOP:
                return "STOP"
            case StatusEnum.OPERATION_RESUMED|StatusEnum.DIRECT_RESUMED:
                return "RESUMED"
            case _:
                return "NULL"

    def to_dict(self) -> MultiLanguageDictWithId:
        result:MultiLanguageDictWithId = {
            "id": self.name,
            "ja": self.format_ja(),
            "en": self.format_en(),
            "ko": self.format_ko(),
            "zh-Hans": self.format_zh_CN(),
            "zh-Hant": self.format_zh_TW(),
        }
        # result["ja-Hrkt"] = self.
        return result

class StatusPlacement(StringEnum):

    OCCASION = auto()
    MAIN = auto()
    WITH = auto()

class StatusIcon(StringEnum):

    NULL = auto()

    CIRCLE = auto()
    CROSS = auto()
    DIRECT_STOP = auto()
    EXCLAMATION = auto()
    QUESTION = auto()
    TRIANGLE = auto()

class Status:

    enum: StatusEnum = StatusEnum.NULL
    modifiers: list[StatusModifier]
    sub_status: Optional[Status] = None
    last_statuses: list[Status]
    _placement: StatusPlacement

    def __init__(self, placement: StatusPlacement = StatusPlacement.WITH) -> None:
        self.modifiers = [StatusModifier()]
        self.last_statuses = []
        self._placement = placement

    def DELAY_AND_CANCEL(self) -> None:
        self.enum = StatusEnum.DELAY
        self.sub_status = Status()
        self.sub_status.enum = StatusEnum.SOME_TRAIN_CANCEL

    def supplement(self):
        if self.enum.get_suffix() != "RESUMED":
            return
        if self.modifiers != []:
            return

        now_prefix = self.enum.get_prefix()
        for status in self.last_statuses:
            last = status.enum
            if last.get_prefix() != now_prefix:
                continue
            if last.get_suffix() in ["STOP","RESUMED"]:
                self.modifiers = status.modifiers
                return

    def find_all_enums(self) -> list[StatusEnum]:
        if self.sub_status:
            return [self.enum]+self.sub_status.find_all_enums()
        else:
            return [self.enum]

    def find_all_lines(self) -> list[LineName]:
        result: list[LineName] = []
        for modifier in self.modifiers:
            if modifier.lines:
                result += modifier.lines
        return result

    def find_all_others(self) -> list[str]:
        result: list[str] = []
        for modifier in self.modifiers:
            if modifier.others:
                result += modifier.others
        return result

    def has_some_train(self) -> bool:
        for modifier in self.modifiers:
            if modifier.some_train:
                return True
        if self.sub_status:
            return self.sub_status.has_some_train()
        else:
            return False

    def build_places_ja(self, postfix: str = "") -> str:
        result: list[str] = []
        for modifier in self.modifiers:
            place_text = modifier.build_place_ja()
            if place_text:
                result.append(place_text)
        if result and (concat := concat_ja(result)):
            return concat+postfix
        else:
            return ""

    def build_modifiers_ja(self, postfix: str = "", exclude_some_train: bool = False) -> str:
        result: list[str] = []
        modifier_count = len(self.modifiers)
        for i, modifier in enumerate(self.modifiers):
            if i == modifier_count-1:  # is last loop
                modifier_text = modifier.build_ja(
                                            exclude_some_train=exclude_some_train)
            else:
                modifier_text = modifier.build_ja(
                                            exclude_some_train=True)
            if modifier_text:
                result.append(modifier_text)
        if result and (concat := concat_ja(result)):
            return concat+postfix
        else:
            return ""

    def build_ja(self):
        result: list[str] = []
        if self.sub_status:
            result.append(self.build_modifiers_ja("に"))
            match self.enum:
                case StatusEnum.DELAY:
                    result.append("遅れと")
                case StatusEnum.DESTINATION_CHANGE:
                    result.append("行先変更と")
                case StatusEnum.SOME_TRAIN_CANCEL:
                    result.append("運休と")
                case _:
                    result.append("{invalid status}と")
            result.append(self.sub_status.build_ja())
            return "".join(result)

        if self._placement == StatusPlacement.WITH:
            result.append(self.build_modifiers_ja("に"))
            match self.enum:
                case StatusEnum.DELAY:
                    result.append("遅れがでています。")
                case StatusEnum.DESTINATION_CHANGE:
                    result.append("行先変更がでています。")
                case StatusEnum.SOME_TRAIN_CANCEL:
                    result.append("運休がでています。")
                case _:
                    result.append("{invalid status}がでています。")
            return "".join(result)

        match self.enum:
            case StatusEnum.UNKNOWN:
                result.append(self.build_modifiers_ja("に") + "{unknown status}。")
            case StatusEnum.NORMAL:
                result.append("概ね平常通り運転しています。")
            case StatusEnum.DELAY:
                result.append(self.build_modifiers_ja("に") + "遅れがでています。")
            case StatusEnum.OPERATION_STOP:
                result.append(self.build_modifiers_ja("で") + "運転を見合わせています。")
            case StatusEnum.OPERATION_RESUMED:
                result.append(self.build_modifiers_ja("は") + "運転を再開しました。")
            case StatusEnum.DESTINATION_CHANGE:
                result.append(self.build_modifiers_ja("に") + "行先変更がでています。")
            case StatusEnum.TURN_BACK_OPERATION:
                result.append(self.build_modifiers_ja("で") + "折返し運転を行っています。")
            case StatusEnum.DIRECT_STOP:
                if lines := self.find_all_lines():
                    lines_texts:list[str] = []
                    for line in lines:
                        if line_text := line.format_ja():
                            lines_texts.append(line_text)
                    result.append( concat_ja(lines_texts)+"への" )
                result.append("直通運転を中止しています。")
            case StatusEnum.DIRECT_RESUMED:
                if lines := self.find_all_lines():
                    lines_texts:list[str] = []
                    for line in lines:
                        if line_text := line.format_ja():
                            lines_texts.append(line_text)
                    result.append( concat_ja(lines_texts)+"への" )
                result.append("直通運転を再開しました。")
            case StatusEnum.STOP | StatusEnum.RESUMED:
                if others := self.find_all_others():
                    others_texts:list[str] = []
                    for other in others:
                        if other:
                            others_texts.append(other)
                    result.append( concat_ja(others_texts) )
                else:
                    result.append("{invalid modifier}")
                if self.enum == StatusEnum.STOP:
                    result.append("を中止しています。")
                else:
                    result.append("は再開しました。")
            case StatusEnum.SOME_TRAIN_CANCEL:
                result.append(self.build_modifiers_ja("で", True))
                if result[-1].endswith("行き列車で"):
                    result[-1] = result[-1][:-3]
                result.append("一部列車が運休となっています。")
            case StatusEnum.SOME_SECTION_CANCEL:
                result.append(self.build_modifiers_ja("で", True) + "区間運休となっています。")
            case _:
                result.append(self.build_modifiers_ja("に") + "{invalid status}。")
        return "".join(result)

    def build_main_en(self) -> tuple[str,str,str]:

        """
        pre_line the XX line post_line status_text post_status. post_script
        """

        pre_line: list[str]
        post_line: list[str]
        status_text: str = "has {unknown} operation"
        post_status: list[str]
        post_script: str = ""

        modifier = self.modifiers[0]
        id_list = self.find_all_enums()

        if len(id_list)>1:
            pre_line, post_line, post_status = modifier.build_main_en("of")
            post_line.append("has")
            valid_status_texts: list[str] = []
            for id in id_list:
                match id:
                    case StatusEnum.DELAY:
                        valid_status_texts.append("delayed")
                    case StatusEnum.DESTINATION_CHANGE:
                        valid_status_texts.append("{unknown}") # TODO
                    case StatusEnum.SOME_TRAIN_CANCEL:
                        valid_status_texts.append("suspended")
                    case _:
                        pass
            if valid_status_texts and (concat := concat_en(valid_status_texts)):
                status_text = concat + " operation"
            else:
                return "", "", ""
        else:
            pre_line, post_line, post_status = ([""],[""],[""])
            match self.enum:
                case StatusEnum.UNKNOWN:
                    pre_line, post_line, post_status = modifier.build_main_en("of")
                case StatusEnum.NORMAL:
                    status_text = "has normal operation"
                case StatusEnum.DELAY:
                    pre_line, post_line, post_status = modifier.build_main_en("of")
                    if modifier and modifier.some_train:
                        status_text = "has delayed operation"
                    else:
                        status_text = "is being delayed"
                case StatusEnum.OPERATION_STOP:
                    pre_line, post_line, post_status = modifier.build_main_en("on")
                    status_text = "is temporarily being stopped"
                case StatusEnum.OPERATION_RESUMED:
                    pre_line, post_line, post_status = modifier.build_main_en("on")
                    status_text = "was temporarily being stopped"
                case StatusEnum.DESTINATION_CHANGE:
                    pass # TODO research
                case StatusEnum.TURN_BACK_OPERATION:
                    pass # TODO research
                case StatusEnum.DIRECT_STOP:
                    status_text = "currently has no through service to some or all of lines"
                    post_script = "Direct operation stop: %s." % ",".join([ line.format_en() for line in self.find_all_lines()])
                case StatusEnum.DIRECT_RESUMED:
                    pass # TODO research
                case StatusEnum.SOME_TRAIN_CANCEL:
                    pre_line, post_line, post_status = modifier.build_main_en("of", True)
                    status_text = "is out of service"
                case _:
                    status_text = "has {invalid} operation"

        mid:list[str] = [ single for single in post_line+[status_text]+post_status if single ]
        return " ".join(pre_line), " ".join(mid), post_script

    def build_sub_en(self) -> str:

        match self.enum:
            case StatusEnum.DIRECT_STOP:
                return "We have stopped direct operation to the %s." % self.modifiers[0].lines[0].format_en()
            case _:
                return ""
