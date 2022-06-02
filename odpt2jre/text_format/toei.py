
import copy
import re
import odpttraininfo as odpt
from ..intermediate_components import *
from . import common
from .field_string import embed_field, find_all_field, find_field

staList = {
    "Toei.Asakusa": [["[Sta:20001]","[Sta:6001]","[Sta:20006]","[Sta:29]","[Sta:427]","[Sta:1003]"]]
}

def to_jre(info:odpt.TrainInformation) -> list[TrainInformation]:

    if not info.train_information_status:
        return [common.normal_operation(info,remove_macrons=True)]

    result:TrainInformation = TrainInformation(info)
    result.text_raw.ja = embed_field( info.train_information_text.ja )

    if result.line_header.en:
        result.line_header.en = common.removeMacrons(result.line_header.en)

    info_text = result.text_raw.ja

    if _match := re.fullmatch( r".+?は、(.+?)(のため|の影響)(.+?)", info_text ):
        cause_text = _match[1]
        main_status_text = _match[3]
    elif _match := re.fullmatch( r".+?は、(.+?)", info_text ):
        cause_text = ""
        main_status_text = _match[1]
    else:
        return [common.normal_operation(info,remove_macrons=True)]

    if _match := re.fullmatch( r"(.*?)運?転?を?見合わせていましたが(.*?)運転を?再開し(.+?)", main_status_text ):
        main_status_text = _match[3]
        result.status_occasion.enum = StatusEnum.OPERATION_RESUMED
        for field in find_all_field(_match[1]):
            match field[0]:
                case BetweenStations.header:
                    result.status_occasion.modifiers[0].sections.append(BetweenStations(field[1]))
        if _match[2].endswith("は") and not result.status_occasion.modifiers[0].sections:
            result.status_main.enum = StatusEnum.OPERATION_STOP
            result.status_occasion.enum = StatusEnum.NULL
            try:
                sections = copy.deepcopy(staList[ result.line_header.id ])
                stopSections:list[list[str]] = []
                for field in find_all_field(_match[2]):
                    match field[0]:
                        case BetweenStations.header:
                            stopSections.append( BetweenStations(field[1]).args )

                for stopSection in stopSections:
                    n_sections:list[list[str]] = []
                    for section in sections:
                        if stopSection[0] in section and stopSection[-1] in section:
                            start = section.index(stopSection[0])
                            end = section.index(stopSection[-1])
                            if end<start:
                                start, end = end, start
                            if start!=0:
                                start+=1
                            if end==len(section)-1:
                                end+=1
                            if start==0 or end==len(section):
                                del section[start:end]
                                n_sections.append(section)
                            else:
                                n_sections.append(section[0:start])
                                n_sections.append(section[end:])
                        else:
                            n_sections.append(section)
                    sections = n_sections

                for section in sections:
                    if len(section)>1:
                        result.status_main.modifiers[0].sections.append(BetweenStations("[BetweenSta:%s,%s]" %(section[0],section[-1])))
            except:
                pass
        else:
            if field := find_field(_match[2]):
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


    if "[Cause:47]" in main_status_text:
        result.status_main.enum = StatusEnum.DELAY
        if "運休" in main_status_text:
            result.status_main.DELAY_AND_CANCEL()
        elif "行先" in main_status_text and "変更" in main_status_text:
            result.status_main.sub_status = Status()
            result.status_main.sub_status.enum = StatusEnum.DESTINATION_CHANGE
    elif "運休" in main_status_text:
        result.status_main.enum = StatusEnum.SOME_TRAIN_CANCEL
    elif "運転を見合わせ" in main_status_text:
        result.status_main.enum = StatusEnum.OPERATION_STOP
    elif "行先" in main_status_text and "変更" in main_status_text:
        result.status_main.enum = StatusEnum.DESTINATION_CHANGE

    if "一部" in main_status_text:
        result.status_main.modifiers[0].some_train = True

    return [result]
