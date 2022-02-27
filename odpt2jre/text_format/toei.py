
import re
import odpttraininfo as odpt
from ..intermediate_components import *
from . import common
from .field_string import embed_field, find_all_field, find_field


def to_jre(info:odpt.TrainInformation) -> list[TrainInformation]:

    if not info.train_information_status:
        return [common.normal_operation(info)]

    result:TrainInformation = TrainInformation(info)
    result.text_raw.ja = embed_field( info.train_information_text.ja )

    info_text = result.text_raw.ja

    if match := re.fullmatch( r".+?は、(.+?)(のため|の影響)(.+?)", info_text ):
        cause_text = match[1]
        main_status_text = match[3]
    elif match := re.fullmatch( r".+?は、(.+?)", info_text ):
        cause_text = ""
        main_status_text = match[1]
    else:
        return [common.normal_operation(info)]

    if match := re.fullmatch( r"(.*?)運転を見合わせていましたが、(.*?)運転を再開し(.+?)", main_status_text ):
        main_status_text = match[3]
        result.status_occasion.enum = StatusEnum.OPERATION_RESUMED
        if field := find_field(match[2]):
            match field[0]:
                case ClockTime.header:
                    result.time_resume = ClockTime(field[1])

    cause_field_list = find_all_field(cause_text)

    for field in cause_field_list:
        match field[0]:
            case CauseName.header:
                result.cause = Cause(field[1])
            case ClockTime.header:
                result.time_occur = ClockTime(field[1])

    if result.cause:
        for field in cause_field_list:
            match field[0]:
                case LineName.header:
                    result.cause.lines.append( LineName(field[1]) )
                case SingleStation.header:
                    result.cause.sections.append( SingleStation(field[1]) )
                case BetweenStations.header:
                    result.cause.sections.append( BetweenStations(field[1]) )

    main_field_list = find_all_field(main_status_text)

    for field in main_field_list:
        match field[0]:
            case Direction.header:
                result.status_main.modifiers[0].direction = Direction(field[1])
            case BetweenStations.header:
                result.status_main.modifiers[0].sections.append(BetweenStations(field[1]))


    if "遅延" in main_status_text:
        result.status_main.enum = StatusEnum.DELAY
        if "運休" in main_status_text:
            result.status_main.DELAY_AND_CANCEL()
    elif "運休" in main_status_text:
        result.status_main.enum = StatusEnum.SOME_TRAIN_CANCEL
    elif "運転を見合わせ" in main_status_text:
        result.status_main.enum = StatusEnum.OPERATION_STOP

    if "一部" in main_status_text:
        result.status_main.modifiers[0].some_train = True

    return [result]
