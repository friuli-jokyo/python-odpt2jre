from .output_dict import MultiLanguageDict
from .ordinal_direction import OrdinalDirection
from .multi_language_expression import MultiLanguageExpression, MultiLanguageExpressionWithTable


class StationName(MultiLanguageExpressionWithTable, header="Sta"):
    pass

class SingleStation(MultiLanguageExpression, header="SingleSta"):

    _station: StationName

    def __init__(self, field: str) -> None:
        super().__init__(field)
        if len(self._args)==1:
            self._station = StationName(self._args[0])
        else:
            raise ValueError("Invalid argument number.")

    def format_ja(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"東京駅"``
        """
        return self._station.format_ja()+"駅"

    def format_en(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"Tōkyō Station"``
        """
        return self._station.format_en()+" Station"

    def format_ko(self, separation: bool = False) -> str:
        """
        Parameters
        ----------
        separation : bool, optional
            This option is disabled at this class , by default False

        Returns
        -------
        str
            e.g. ``"도쿄역"``
        """
        return self._station.format_ko()+"역"

    def format_zh_CN(self, separation: bool = False) -> str:
        """
        Parameters
        ----------
        separation : bool, optional
            This option is disabled at this class , by default False

        Returns
        -------
        str
            e.g. ``"东京站"``
        """
        return self._station.format_ko()+"站"

    def format_zh_TW(self, separation: bool = False) -> str:
        """
        Parameters
        ----------
        separation : bool, optional
            This option is disabled at this class , by default False

        Returns
        -------
        str
            e.g. ``"東京站"``
        """
        return self._station.format_ko()+"站"

class BetweenStations(MultiLanguageExpression, header="BetweenSta"):

    _stations: list[StationName]

    def __init__(self, field: str) -> None:
        super().__init__(field)
        if len(self._args) < 2:
            raise ValueError("Lack of arguments")
        else:
            self._stations = []
            for arg in self._args:
                self._stations.append( StationName(arg) )

    def format_ja(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"東京～新宿駅間"``
        """
        station_names = [station.format_ja() for station in self._stations]
        return "～".join(station_names)+"駅間"

    def format_en(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"Between Tōkyō and Shinjuku Station"``
        """
        station_names = [station.format_en() for station in self._stations]
        return "Between " + " and ".join(station_names) + " Station"

    def format_ko(self, separation: bool = False) -> str:
        """
        Parameters
        ----------
        separation : bool, optional
            If True, word separation is enabled, by default False

        Returns
        -------
        str
            e.g. ``"도쿄～신주쿠역간"``
        """
        station_names = [station.format_ko() for station in self._stations]
        if separation:
            return " ～ ".join(station_names)+" 역간"
        else:
            return "～".join(station_names)+"역간"

    def format_zh_CN(self, separation: bool = False) -> str:
        """
        Parameters
        ----------
        separation : bool, optional
            If True, word separation is enabled, by default False

        Returns
        -------
        str
            e.g. ``"东京～新宿站间"``
        """
        station_names = [station.format_zh_CN() for station in self._stations]
        if separation:
            return " ～ ".join(station_names)+" 站间"
        else:
            return "～".join(station_names)+"站间"

    def format_zh_TW(self, separation: bool = False) -> str:
        """
        Parameters
        ----------
        separation : bool, optional
            If True, word separation is enabled, by default False

        Returns
        -------
        str
            e.g. ``"東京～新宿站之間"``
        """
        station_names = [station.format_zh_TW() for station in self._stations]
        if separation:
            return " ～ ".join(station_names)+" 站之間"
        else:
            return "～".join(station_names)+"站之間"

    def to_dict(self) -> MultiLanguageDict:
        result:MultiLanguageDict = {
            "ja": "～".join([ station.format_ja() for station in self._stations])
        }
        if en := " ~ ".join([ station.format_en() for station in self._stations]):
            result["en"] = en
        if ko := " ~ ".join([ station.format_ko() for station in self._stations]):
            result["ko"] = ko
        if zh_CN := " ~ ".join([ station.format_zh_CN() for station in self._stations]):
            result["zh-Hans"] = zh_CN
        if zh_TW := " ~ ".join([ station.format_zh_TW() for station in self._stations]):
            result["zh-Hant"] = zh_TW
        return result

class OrdinalDirectionFromStaton(MultiLanguageExpression, header="OrdinalFromSta"):
    """
    Note
    ----
    This class supports only Japanese.

    """
    _station: SingleStation
    _direction: OrdinalDirection

    def __init__(self, field: str ) -> None:
        super().__init__(field)
        if len(self._args)==2:
            self._station = SingleStation(self._args[0])
            self._direction = OrdinalDirection.from_ja(self._args[1])


    def format_ja(self) -> str:
        """
        Returns
        -------
        str
            e.g. ``"東京駅以北"``
        """
        return self._station.format_ja()+"以"+self._direction.format_ja()

    def format_en(self) -> str:
        """

        """
        return ""

    def format_ko(self) -> str:
        """

        """
        return ""

    def format_zh_CN(self) -> str:
        """

        """
        return ""

    def format_zh_TW(self) -> str:
        """

        """
        return ""
