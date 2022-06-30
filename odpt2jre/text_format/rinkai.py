
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

    info_texts = result.text_raw.ja.split("。")

    # 「～の(影響で/のため)～」を分割
    for i in range(len(info_texts)):
        if (_match := re.fullmatch(r"(.+?)(の影響で|のため)(.+?)",info_texts[i])) and _match[3] != "す":
            info_texts = info_texts[:i] + [ _match[3], _match[1]+"の影響で" ] + info_texts[i:]

    for info_text in info_texts:
        # 運転再開構文
        if info_text.startswith("運転を見合わせていましたが"):
            result.status_occasion.enum = StatusEnum.OPERATION_RESUMED
            for field in find_all_field(info_text):
                match field[0]:
                    case ClockTime.header:
                        result.time_resume = ClockTime(field[1])

        # 運転状況
        if info_text.endswith("遅れがでています") or info_text.endswith("ダイヤが乱れています"):
            result.status_main.enum = StatusEnum.DELAY
        elif info_text.endswith("運転を見合わせています") and result.status_occasion.enum != StatusEnum.OPERATION_RESUMED:
            result.status_main.enum = StatusEnum.OPERATION_STOP
        elif info_text.endswith("一部列車に運休が出ています"):
            result.status_main.enum = StatusEnum.SOME_TRAIN_CANCEL
            result.status_main.modifiers[0].some_train = True

    # 直通中止/再開はメインの状況がある場合サブに回す
    for info_text in info_texts:
        if _match := re.search( f"({LineName.regex})との直通運転を(中止し|見合わせていましたが、直通運転を再開し)", info_text ):
            if result.status_main.enum == StatusEnum.NULL:
                if _match[3] == "中止し":
                    result.status_main.enum = StatusEnum.DIRECT_STOP
                    result.status_main.modifiers[0].lines.append(LineName(_match[1]))
                else:
                    result.status_occasion.enum = StatusEnum.DIRECT_RESUMED
                    result.status_occasion.modifiers[0].lines.append(LineName(_match[1]))

            else:
                status = Status(StatusPlacement.MAIN)
                if _match[3] == "中止し":
                    status.enum = StatusEnum.DIRECT_STOP
                else:
                    status.enum = StatusEnum.DIRECT_RESUMED
                status.modifiers[0].lines.append(LineName(_match[1]))
                result.sentences_sub.append( status )

    # 原因
    for info_text in info_texts:
        if "影響" in info_text:
            field_list = find_all_field(info_text)

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