from .multi_language_expression import MultiLanguageExpression

HALF_TO_FULL = str.maketrans(
    {
        "0": "０",
        "1": "１",
        "2": "２",
        "3": "３",
        "4": "４",
        "5": "５",
        "6": "６",
        "7": "７",
        "8": "８",
        "9": "９",
    }
)


class ClockTime(MultiLanguageExpression, header="CLK"):
    """Store time of day.

    Parameters
    ----------
    field : str
        String format looks like ``"[CLK12,00]"``

    Raises
    ------
    ValueError
        If ``field`` is invalid.
    """
    hour: int = -1
    minute: int = 0

    def __init__(self, field: str) -> None:
        super().__init__(field)
        if len(self._args)==2:
            self.hour = int(self._args[0]) % 24
            self.minute = int(self._args[1])
            if not self.__bool__():
                raise ValueError("Invalid minute.")
        else:
            raise ValueError("Field string doesn't match.")

    def __bool__(self) -> bool:
        if 0 <= self.hour < 24 and 0 <= self.minute < 60:
            return True
        return False

    def _format_with_cologne(self, twenty_four_hours:bool = False) -> str:
        """
        Returns
        -------
        str
            e.g. ``"1:23"``
        """
        if self.__bool__():
            if self.hour <= 12 or twenty_four_hours:
                return str(self.hour) + ":"+str(self.minute).zfill(2)
            else:
                return str(self.hour-12) + ":"+str(self.minute).zfill(2)
        else:
            return ""

    def format_24h(self) -> str:
        return self._format_with_cologne(twenty_four_hours=True)

    def format_ja(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"１時２３分"``
        """
        if self.__bool__():
            return (str(self.hour).translate(HALF_TO_FULL)+"時"
                    + str(self.minute).zfill(2).translate(HALF_TO_FULL)+"分")
        else:
            return ""

    def format_en(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"1:23 AM"``
        """
        if self.__bool__():
            if self.hour <= 12:
                return self._format_with_cologne() + " AM"
            else:
                return self._format_with_cologne() + " PM"
        else:
            return ""

    def format_ko(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"오전1:23"``
        """
        if self.__bool__():
            if self.hour <= 12:
                return "오전" + self._format_with_cologne()
            else:
                return "오후" + self._format_with_cologne()
        else:
            return ""

    def format_zh_CN(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"上午1:23"``
        """
        if self.__bool__():
            if self.hour <= 12:
                return "上午" + self._format_with_cologne()
            else:
                return "下午" + self._format_with_cologne()
        else:
            return ""

    def format_zh_TW(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"上午1:23"``
        """
        if self.__bool__():
            if self.hour <= 12:
                return "上午" + self._format_with_cologne()
            else:
                return "下午" + self._format_with_cologne()
        else:
            return ""
