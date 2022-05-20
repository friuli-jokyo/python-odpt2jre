
import re
import odpttraininfo as odpt
from ..intermediate_components import *
from . import common
from .field_string import embed_field, find_all_field


def to_jre(info:odpt.TrainInformation) -> list[TrainInformation]:

    if not info.train_information_status or info.train_information_text.ja=="ただいまの時間は、運行情報のサービス提供時間外です。":
        return [common.normal_operation(info)]

    result:TrainInformation = TrainInformation(info)
    result.text_raw.ja = embed_field( info.train_information_text.ja )

    info_text = result.text_raw.ja.split("。")

    if len(info_text) >= 1 and (match := re.fullmatch(r"(.+?)(の影響で|のため)(.+?)",info_text[0])):
        info_text = [ match[3], match[1]+"の影響で" ] + info_text[1:]
    if len(info_text) >= 1:
        if info_text[0].startswith("運転を見合わせていましたが"):
            result.status_occasion.enum = StatusEnum.OPERATION_RESUMED
            for field in find_all_field(info_text[0]):
                match field[0]:
                    case ClockTime.header:
                        result.time_resume = ClockTime(field[1])

        if info_text[0].endswith("遅れがでています") or info_text[0].endswith("ダイヤが乱れています"):
            result.status_main.enum = StatusEnum.DELAY
        elif info_text[0].endswith("運転を見合わせています") and result.status_occasion.enum != StatusEnum.OPERATION_RESUMED:
            result.status_main.enum = StatusEnum.OPERATION_STOP
    if len(info_text) >= 1:
        if match := re.search( f"({LineName.regex})との直通運転を中止して、", info_text[0] ):
            if result.status_main.enum == StatusEnum.NULL:
                result.status_main.enum = StatusEnum.DIRECT_STOP
                result.status_main.modifiers[0].lines.append(LineName(match[1]))
            else:
                status = Status(StatusPlacement.MAIN)
                status.enum = StatusEnum.DIRECT_STOP
                status.modifiers[0].lines.append(LineName(match[1]))
                result.statuses_sub.append( status )

    if len(info_text) >= 2 and "影響" in info_text[1]:
        field_list = find_all_field(info_text[1])

        for field in field_list:
            match field[0]:
                case CauseName.header:
                    result.cause = Cause(field[1])

        for field in field_list:
            match field[0]:
                case LineName.header:
                    if result.cause and field[1] != "[Line:TWR.Rinkai]":
                        result.cause.lines.append(LineName(field[1]))
                case SingleStation.header:
                    if result.cause:
                        result.cause.sections.append(SingleStation(field[1]))
                case BetweenStations.header:
                    if result.cause:
                        result.cause.sections.append(BetweenStations(field[1]))

    return [result]
