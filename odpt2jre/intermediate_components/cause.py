from __future__ import annotations

from typing import Optional

from .common import concat_ja
from .company import CompanyName
from .line import LineName
from .multi_language_expression import (MultiLanguageExpression,
                                        MultiLanguageExpressionWithTable)
from .station import BetweenStations, SingleStation


class CauseName(MultiLanguageExpressionWithTable, header="Cause"):
    pass

class Cause(MultiLanguageExpression, header=""):

    causes: list[CauseName]
    companies: list[CompanyName]
    lines: list[LineName]
    sections: list[SingleStation|BetweenStations]
    sub_cause: Optional[Cause] = None

    def __init__(self, cause:Optional[str] = None) -> None:
        self.causes = []
        self.companies = []
        self.lines = []
        self.sections = []
        if cause:
            self.causes.append(CauseName(cause))

    def format_ja(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"東京駅での異音の確認の影響で、"``
        """
        result: list[str] = []
        if self.causes:
            if self.companies:
                temp_companies: list[str] = []
                for company in self.companies:
                    if name := company.format_ja():
                        temp_companies.append(name+"管内")
                result.append(concat_ja(temp_companies))
                result.append("での")
            elif self.lines:
                temp_lines: list[str] = []
                for line in self.lines:
                    if name := line.format_ja():
                        if name[-1] == "線":
                            temp_lines.append(name+"内")  # ○○線内
                        else:
                            temp_lines.append(name)  # 中央・総武各駅停車 など
                result.append(concat_ja(temp_lines))
                result.append("での")
            elif self.sections:
                temp_sections: list[str] = []
                for section in self.sections:
                    if name := section.format_ja():
                        temp_sections.append(name)
                result.append(concat_ja(temp_sections))
                result.append("での")

            temp_causes: list[str] = []
            for cause in self.causes:
                if name := cause.format_ja():
                    temp_causes.append(name)
            if temp_causes:
                result.append(concat_ja(temp_causes))
                if self.sub_cause:
                    result.append("および")
                    result.append(self.sub_cause.format_ja()[:-5]) # remove "の影響で、"
                result.append("の影響で、")
                return "".join(result)
            else:
                return ""
        else:
            return ""

    def format_en(self, time_str:str = "" ) -> str:
        """
        Returns
        -------
        str
            e.g. ``"due to Unidentified noise at Tōkyō Station"```
        """
        result: list[str] = []
        if self.causes and (cause := self.causes[0].format_en()):
            result.append("due to")
            result.append( cause )
            if time_str:
                result.append("that happened around")
                result.append(time_str)
            if self.companies and (company := self.companies[0].format_en()):
                result.append("on the")
                result.append( company )
            elif self.lines and (line := self.lines[0].format_en()):
                result.append("on the")
                result.append( line )
            elif self.sections and (section := self.sections[0].format_en()):
                if time_str:
                    result.append("in")
                else:
                    result.append("at")
                result.append( section )
            return " ".join(result)
        else:
            return ""

    def format_ko(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"도쿄역에서 발생한 이상음 확인의 영향으로"``
        """
        result: list[str] = []
        if self.causes and (cause := self.causes[0].format_ko()):
            if self.companies and (company := self.companies[0].format_ko()):
                result.append( company ) # {CompanyName}
                result.append("내에서") # 内で
                result.append("발생한") # 発生した
            elif self.lines and (line := self.lines[0].format_ko()):
                result.append( line ) # {LineName}
                result.append("내에서") # 内で
                result.append("발생한") # 発生した
            elif self.sections and (section := self.sections[0].format_ko(separation=True)):
                result.append( section+"에서" ) # {BetweenSta}で
                result.append("발생한") # 発生した
            result.append( cause+"의" ) # {cause}の
            result.append("영향으로") # 影響で
            return " ".join(result)
        else:
            return ""

    def format_zh_CN(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"受东京站确认异常音的影响"``
        """
        result: list[str] = []
        if self.causes and (cause := self.causes[0].format_zh_CN()):
            result.append("受")
            if self.companies and (company := self.companies[0].format_zh_CN()):
                result.append( company+"内" ) # {CompanyName}での
            elif self.lines and (line := self.lines[0].format_zh_CN()):
                result.append( line+"内" ) # {LineName}での
            elif self.sections and (section := self.sections[0].format_zh_CN(separation=True)):
                result.append( section ) # {BetweenSta}での
            result.append( cause+"的影响" ) # {cause}の影響で
            return "".join(result)
        else:
            return ""

    def format_zh_TW(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"因東京站確認異常音的影響"``
        """
        result: list[str] = []
        if self.causes and (cause := self.causes[0].format_zh_TW()):
            result.append("因")
            if self.companies and (company := self.companies[0].format_zh_TW()):
                result.append( company+"內的" ) # {CompanyName}での
            elif self.lines and (line := self.lines[0].format_zh_TW()):
                result.append( line+"內的" ) # {LineName}での
            elif self.sections and (section := self.sections[0].format_zh_TW(separation=True)):
                result.append( section ) # {BetweenSta}での
            result.append( cause+"的影響" ) # {cause}の影響で
            return "".join(result)
        else:
            return ""
