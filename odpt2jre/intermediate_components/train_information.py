from __future__ import annotations

from datetime import datetime
from typing import Optional

import odpttraininfo as odpt
from odpttraininfo.odpt_components import MultiLanguageString

from .direction import Direction
from .station import BetweenStations
from .output_dict import TrainInformationDict, remove_unimportant

from .common import concat_ja

from .cause import Cause
from .datetime import ClockTime
from .line import LineName
from .status import Status, StatusEnum, StatusPlacement


class TrainInformation:

    text_raw: MultiLanguageString
    text_info: MultiLanguageString

    status_main: Status
    status_occasion: Status
    statuses_sub: list[Status]

    cause: Optional[Cause] = None

    time_occur: Optional[ClockTime] = None
    time_resume: Optional[ClockTime] = None
    time_resume_changed:bool = False

    line_header: LineName
    line_body: LineName

    date: datetime
    valid: Optional[datetime] = None

    def __init__(self, info:Optional[odpt.TrainInformation] = None) -> None:
        self.text_raw = MultiLanguageString()
        self.text_info = MultiLanguageString()

        self.status_main = Status(StatusPlacement.MAIN)
        self.status_occasion = Status(StatusPlacement.OCCASION)
        self.statuses_sub = []

        if info:
            self.line_header = LineName(info.get_line())
            self.line_body = LineName(info.get_line())
            self.date = info.date
            if info.valid:
                self.valid = info.valid
        else:
            self.line_header = LineName("[Line:Debug]")
            self.line_body = LineName("[Line:Debug]")
            self.date = datetime.now()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            self_dict = remove_unimportant(self.to_dict())
            __o_dict = remove_unimportant(__o.to_dict())
            for key in self_dict.keys() & __o_dict.keys():
                if self_dict.get(key, None) != __o_dict.get(key, None):
                    return False
            return True
        raise NotImplementedError

    @property
    def status_enum_header(self) -> StatusEnum:
        if self.status_occasion:
            match self.status_occasion.enum:
                case StatusEnum.OPERATION_RESUMED:
                    return StatusEnum.OPERATION_RESUMED
                case StatusEnum.DIRECT_RESUMED:
                    return StatusEnum.DIRECT_RESUMED
                case _:
                    pass
        if self.time_resume:
            if self.status_main.enum==StatusEnum.OPERATION_STOP:
                return StatusEnum.OPERATION_WILL_RESUME
        return self.status_main.enum

    @property
    def occasion(self) -> bool:
        if self.status_occasion.enum != StatusEnum.NULL:
            return True
        else:
            return False

    @property
    def direction(self) -> Direction:
        if self.occasion:
            status = self.status_occasion
        else:
            status = self.status_main
        if status.modifiers[0].direction:
            return status.modifiers[0].direction
        else:
            return Direction("[Direction:INBOUND_AND_OUTBOUND]")

    @property
    def section(self) -> Optional[BetweenStations]:
        if self.occasion:
            status = self.status_occasion
        else:
            status = self.status_main
        if status.modifiers[0].sections:
            section = status.modifiers[0].sections[0]
            match section:
                case BetweenStations():
                    return section
                case _:
                    pass

    @classmethod
    def list_diff(cls, new: list[TrainInformation], old: list[TrainInformation]) -> tuple[list[TrainInformation], list[TrainInformation]]:

        added = [info_new for info_new in new if info_new not in old]
        removed = [info_old for info_old in old if info_old not in new]

        return added, removed

    def to_dict(self) -> TrainInformationDict:

        self.status_main.supplement()
        self.status_occasion.supplement()
        for sub in self.statuses_sub:
            sub.supplement()

        if not self.text_info.ja:
            self.text_info.ja = self.build_ja()
        self.text_info.en = self.build_en()

        result:TrainInformationDict = {
            "lineName": self.line_header.to_dict(),
            "cause": None,
            "direction": self.direction.to_dict(),
            "section": {
                "ja": "全線",
                "en": "All lines",
                "ko": "전선",
                "zh-Hans": "全线",
                "zh-Hant": "全線",
            },
            "infoStatus": self.status_enum_header.to_dict(),
            "infoStatusIcon": self.status_enum_header.get_icon().name,
            "infoText": self.text_info.to_dict(),
            "rawText": self.text_raw.to_dict(),
            "causeTime": None,
            "resumeTime": None,
            "date": self.date.isoformat(),
            "valid": None,
        }
        if self.cause:
            result["cause"] = self.cause.causes[0].to_dict()
        if self.section:
            result["section"] = self.section.to_dict()
        if self.time_occur:
            result["causeTime"] = self.time_occur.format_24h()
        if self.time_resume:
            result["resumeTime"] = self.time_resume.format_24h()
        if self.valid:
            result["valid"] = self.valid.isoformat()

        return result

    def build_ja(self) -> str:

        result:str = ""

        result += self.line_body.format_ja() + "は、"

        if not self.time_resume and self.status_main.enum == StatusEnum.OPERATION_STOP:
            if self.time_occur:
                result += self.time_occur.format_ja()+"頃　"

        if self.cause:
            result += self.cause.format_ja()

        if self.status_occasion:
            match self.status_occasion.enum:
                case StatusEnum.OPERATION_RESUMED:
                    result += self.status_occasion.build_modifiers_ja("で")
                    result += "運転を見合わせていましたが、"
                    if self.time_resume:
                        result += self.time_resume.format_ja()+"頃に"
                    result += "運転を再開し"
                case StatusEnum.DIRECT_RESUMED:
                    if lines := self.status_occasion.find_all_lines():
                        lines_texts:list[str] = []
                        for line in lines:
                            if line_text := line.format_ja():
                                lines_texts.append(line_text)
                        result+= concat_ja(lines_texts)+"への"
                    result += "直通運転を中止していましたが、"
                    result += "直通運転を再開し"
                case _:
                    pass

            match self.status_occasion.enum:
                case StatusEnum.OPERATION_RESUMED|StatusEnum.DIRECT_RESUMED:
                    if not self.status_main:
                        result += "ました。"
                    elif self.status_main.modifiers[0] or (self.status_main.enum != StatusEnum.DELAY and not self.status_main.sub_status):
                        result += "、"
                case _:
                    pass
        else:
            if self.status_main.enum == StatusEnum.NULL:
                self.status_main.enum = StatusEnum.NORMAL

        if self.status_main:
            result += self.status_main.build_ja()

        if self.status_main.enum == StatusEnum.OPERATION_STOP:
            if self.time_resume:
                if self.time_resume_changed:
                    result += "運転再開見込は"+self.time_resume.format_ja()+"頃に変更になりました。"
                else:
                    result += "運転再開は"+self.time_resume.format_ja()+"頃を見込んでいます。"
            else:
                pass # result += "運転再開見込みは立っていません。"

        for sub in self.statuses_sub:
            if StatusEnum.SOME_TRAIN_CANCEL in self.status_main.find_all_enums():
                if sub.enum == StatusEnum.SOME_TRAIN_CANCEL:
                    continue

            result += sub.build_ja()

        return result

    def build_en(self) -> str:

        result:str = ""

        if self.occasion:
            status = self.status_occasion
        else:
            if self.status_main.enum == StatusEnum.NULL:
                return ""
            status = self.status_main

        pre_line, post_line, post_script = status.build_main_en()
        if pre_line:
            result += " ".join([pre_line,"the",self.line_body.format_en()])
        else:
            result += " ".join(["The",self.line_body.format_en()])

        if post_line:
            result += " "+post_line

        if self.cause and self.cause.format_en():
            if not self.time_resume and self.status_main.enum == StatusEnum.OPERATION_STOP and self.time_occur:
                result += " "+self.cause.format_en(self.time_occur.format_en())
            else:
                result += " "+self.cause.format_en()

        if self.occasion and status.enum == StatusEnum.OPERATION_RESUMED:
            result += " but has resumed operation"
            if self.status_main.enum == StatusEnum.DELAY:
                if self.status_main.has_some_train():
                    result += " but some trains are delayed"
                else:
                    result += " but is delayed"

        if self.occasion and self.time_resume:
            result += " around "+self.time_resume.format_en()

        result += "."

        if not self.occasion and self.time_resume:
            result += "It is expected to resume operation around %s." % self.time_resume.format_en()

        for sub in self.statuses_sub:
            result += " "+sub.build_sub_en()
        if post_script:
            result += " "+post_script

        return result

    def build_ko(self) -> str:

        result:str = ""

        if self.occasion:
            status = self.status_occasion
        else:
            if self.status_main.enum == StatusEnum.NULL:
                return ""
            status = self.status_main

        result += self.line_body.format_ko() + "은"

        if self.cause:
            result += " "+self.cause.format_ko()

        return result # TODO