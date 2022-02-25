from __future__ import annotations

import csv
import os
import re
from abc import ABC, abstractmethod
from typing import ClassVar


class MultiLanguageExpression(ABC):

    _header: ClassVar[str]

    _field: str

    _args: list[str]

    def __init__(self, field: str) -> None:
        self._field = field
        if args_str := re.fullmatch(f"\\[{self._header}:(.+?)\\]", field):
            self._args = args_str[1].split(",")
        else:
            self._args = []

    def __init_subclass__(cls, header:str) -> None:
        cls._header = header

    def copy(self):
        if not self._field:
            raise ValueError("Field is None.")
        else:
            return type(self)(field=self._field)

    @classmethod
    @property
    def header(cls) -> str:
        return cls._header

    @classmethod
    @property
    def regrex(cls) -> str:
        return str(f"\\[{cls.header}:(.+?)\\]")

    @abstractmethod
    def format_ja(self) -> str:
        """
        Returns
        -------
        str
            Japanese text.
        """
        return ""

    @abstractmethod
    def format_en(self) -> str:
        """
        Returns
        -------
        str
            English text.
        """
        return ""

    @abstractmethod
    def format_ko(self) -> str:
        """
        Returns
        -------
        str
            Korean text.
        """
        return ""

    @abstractmethod
    def format_zh_CN(self) -> str:
        """
        Returns
        -------
        str
            Simplified Chinese text.
        """
        return ""

    @abstractmethod
    def format_zh_TW(self) -> str:
        """
        Returns
        -------
        str
            Traditional Chinese text.
        """
        return ""

class MultiLanguageExpressionWithTable(MultiLanguageExpression, header="None"):

    id: str

    ja: str
    """Japanese text."""

    en: str
    """English text."""

    ko: str
    """Korean text."""

    zh_CN: str
    """Simplified Chinese text."""

    zh_TW: str
    """Traditional Chinese text."""

    _id2text: ClassVar[dict[str,list[str]]]
    _text2id: ClassVar[dict[str,str]]

    def __init__(self, field: str) -> None:
        super().__init__(field)
        if self._args:
            if len(self._args)==1:
                self.id = self._args[0]
            else:
                raise ValueError("Too many arguments.")
        elif id := self._text2id.get(field, None):
            self.id = id
        else:
            self.id = field
        if self.id:
            self.ja = self._id2text[self.id][0]
            try:
                self.en = self._id2text[self.id][1]
                self.ko = self._id2text[self.id][2]
                self.zh_CN = self._id2text[self.id][3]
                self.zh_TW = self._id2text[self.id][4]
            except KeyError:
                pass
            except IndexError:
                pass
        else:
            raise ValueError("Can't find id.")

    def __init_subclass__(cls, header: str) -> None:
        cls.set_table_from_csv(cls.__name__+".csv",cls.__name__+"_alias.csv")
        return super().__init_subclass__(header)

    def format_ja(self) -> str:
        return self.ja

    def format_en(self) -> str:
        return self.en

    def format_ko(self) -> str:
        return self.ko

    def format_zh_CN(self) -> str:
        return self.zh_CN

    def format_zh_TW(self) -> str:
        return self.zh_TW

    def to_dict(self) -> dict[str,str]:
        result:dict[str,str] = {}
        if self.id:
            result["id"] = self.id
        result["ja"] = self.ja
        if self.en:
            result["en"] = self.en
        if self.ko:
            result["ko"] = self.ko
        if self.zh_CN:
            result["zh-Hans"] = self.zh_CN
        if self.zh_TW:
            result["zh-Hant"] = self.zh_TW
        return result

    @classmethod
    def set_table_from_csv(cls, filename_id2text:str, filename_alias:str) -> None:
        id2text: dict[str, list[str]] = {}
        text2id: dict[str, str] = {}
        with open("{}/table/{}".format(os.path.dirname(__file__), filename_id2text), encoding="utf-8") as f:
            data = csv.reader(f)
            for row in data:
                try:
                    id2text[row[0]] = row[1:]
                    text2id[row[1]] = row[0]
                except IndexError:
                    pass
        with open("{}/table/{}".format(os.path.dirname(__file__), filename_alias), encoding="utf-8") as f:
            data = csv.reader(f)
            for row in data:
                try:
                    text2id[row[0]] = row[1]
                except IndexError:
                    pass
        cls._id2text = id2text
        cls._text2id = text2id

    @classmethod
    def embed_field(cls, text:str) -> str:
        for key in sorted(cls._text2id.keys(),key=len,reverse=True):
            field = f"[{cls._header}:{cls._text2id[key]}]"
            text = text.replace(key,field)

        return text
