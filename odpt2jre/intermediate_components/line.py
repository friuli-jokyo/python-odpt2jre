from typing import Optional
from odpt2jre.intermediate_components.direction import Direction
from .multi_language_expression import MultiLanguageExpressionWithTable

class LineName(MultiLanguageExpressionWithTable, header="Line"):

    _direction: Optional[Direction] = None

    def __init__(self, field: str) -> None:
        super().__init__(field, use_raw_text=False)
        if len(self._args) >= 2:
            self._direction = Direction(self._args[1])

    @property
    def has_direction(self) -> bool:
        if self._direction:
            return True
        return False

    def format_ja(self, for_dict:bool = False) -> str:
        if self._direction:
            return super().format_ja()+"（%s）" % self._direction.format_ja()
        else:
            return super().format_ja()

    def format_en(self, in_sentence:bool = False) -> str:
        if self._direction:
            if in_sentence:
                return super().format_en()+" (%s)" % self._direction.format_en(in_sentence=in_sentence)
            else:
                return super().format_en()+"(%s)" % self._direction.format_en(in_sentence=in_sentence)
        else:
            return super().format_en()

    def format_ko(self) -> str:
        if self._direction:
            return super().format_ko()+"(%s)" % self._direction.format_ko()
        else:
            return super().format_ko()

    def format_zh_CN(self, in_sentence:bool = False) -> str:
        if self._direction:
            return super().format_zh_CN()+"（%s）" % self._direction.format_zh_CN(in_sentence=in_sentence)
        else:
            return super().format_zh_CN()

    def format_zh_TW(self, in_sentence:bool = False) -> str:
        if self._direction:
            return super().format_zh_TW()+"（%s）" % self._direction.format_zh_TW(in_sentence=in_sentence)
        else:
            return super().format_zh_TW()
