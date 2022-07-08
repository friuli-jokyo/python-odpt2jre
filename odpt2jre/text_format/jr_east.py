import re

import odpttraininfo as odpt

from odpt2jre.intermediate_components.snippet import SnippetEnum

from .field_string import embed_field, find_all_field, find_field
from ..intermediate_components import *
from . import common

def to_jre(info:odpt.TrainInformation) -> list[TrainInformation]:

    if not info.train_information_status:
        return [common.normal_operation(info)]

    result:list[TrainInformation] = []

    raw_info_text = info.train_information_text.ja
    line_name_regex = r"(車|線|ライン|」|）)は、"
    split_count = len( re.findall(line_name_regex, raw_info_text) )
    split_match = re.fullmatch( r"(.*?。|)" + ( r"([^。]*" + line_name_regex + r".+。)" )*split_count ,raw_info_text )

    if split_match:
        if split_match[1]:
            info_text_list = [split_match[1]]
        else:
            info_text_list = []
        info_text_list += split_match.groups()[1::2]
    else:
        info_text_list = [raw_info_text]

    for info_text in info_text_list:

        gen = TrainInformation(info)
        gen.text_raw.ja = embed_field( info_text )
        gen.text_info.ja = info_text

        main_text = gen.text_raw.ja.split("。")[0]

        if "上野東京ラインは、" in main_text:
            gen.line_header = LineName("JR-East.UenoTokyo")

        if _match := re.fullmatch( r".+?は、(.+の影響で、|)(.+?)", main_text ):
            if _match[1]:
                cause_temp = Cause()
                for field in find_all_field(_match[1]):
                    match field[0]:
                        case ClockTime.header:
                            gen.time_occur = ClockTime(field[1])
                        case CauseName.header:
                            cause_temp.causes.append(CauseName(field[1]))
                            if gen.cause:
                                gen.cause.sub_cause = cause_temp
                            else:
                                gen.cause = cause_temp
                            cause_temp = Cause()
                        case CompanyName.header:
                            cause_temp.companies.append(CompanyName(field[1]))
                        case LineName.header:
                            cause_temp.lines.append(LineName(field[1]))
                        case SingleStation.header:
                            cause_temp.sections.append(SingleStation(field[1]))
                        case BetweenStations.header:
                            cause_temp.sections.append(BetweenStations(field[1]))

            if occasion_match := re.fullmatch( r"(.+?)いましたが、(.+?)再開し(.+?)", _match[2]):
                main_status_text = occasion_match[3]
                if occasion_match[1].endswith("運転を見合わせて"):
                    gen.status_occasion.enum = StatusEnum.OPERATION_RESUMED
                elif occasion_match[1].endswith("直通運転を中止して"):
                    gen.status_occasion.enum = StatusEnum.DIRECT_RESUMED
                if field := find_field(occasion_match[2], ClockTime.header):
                    gen.time_resume = ClockTime(field[1])

                gen.status_occasion.modifiers = gen_modifiers(occasion_match[1])
            else:
                main_status_text = _match[2]

            gen.status_main, snippet = gen_status(main_status_text, StatusPlacement.MAIN)
            if snippet:
                gen.sentences_sub.append(snippet)
        else:
            gen.status_main.enum = StatusEnum.NOTICE

        for sub_text in gen.text_raw.ja.split("。")[1:]:
            if time := re.search( r"運転再開見込は(.+?)に変更になりました", sub_text ):
                if field := find_field(time[1], ClockTime.header):
                    gen.time_resume = ClockTime(field[1])
                    gen.time_resume_changed = True
            elif time := re.search( r"運転再開は(.+?)を見込んでいます", sub_text ):
                if field := find_field(time[1], ClockTime.header):
                    gen.time_resume = ClockTime(field[1])
            elif "運転再開見込は立っていません" in sub_text:
                gen.time_resume_not_known = True
            elif "まもなく運転を再開できる見込みです" in sub_text:
                gen.will_resume_soon = True
            elif "係員が現地に向かっています" in sub_text:
                gen.sentences_sub.append(Snippet(SnippetEnum.STAFF_IS_ON_THE_WAY))
            elif stations := re.fullmatch( r"(.+?)には停車しません", sub_text ):
                snippet = Snippet(SnippetEnum.NOT_STOP_AT_STATION)
                for field in find_all_field(stations[1]):
                    match field[0]:
                        case SingleStation.header:
                            snippet.stations.append(SingleStation(field[1]))
                gen.sentences_sub.append(snippet)
            elif "目的地まで通常より大幅に時間を要する場合があります" in sub_text:
                gen.sentences_sub.append(Snippet(SnippetEnum.MAY_TAKE_LONGER_TIME))
            else:
                if sub_status := gen_status(sub_text, StatusPlacement.MAIN):
                    gen.sentences_sub.append(sub_status[0])

        result += [gen]

    return result

def gen_status(text:str, placement:StatusPlacement) -> tuple[Status, Snippet]:

    ret_status:Status = Status(placement)
    ret_snippet:Snippet = Snippet(SnippetEnum.NULL)
    modifier_text:str = ""

    if _match := re.fullmatch( r"(.*?)(遅れ|行先変更|運休)と(.+)", text ):
        ret_status.sub_status, _ = gen_status(_match[3], StatusPlacement.WITH)
        match _match[2]:
            case "遅れ":
                ret_status.enum = StatusEnum.DELAY
            case "行先変更":
                ret_status.enum = StatusEnum.DESTINATION_CHANGE
            case "運休":
                ret_status.enum = StatusEnum.SOME_TRAIN_CANCEL
            case _:
                pass
        modifier_text = _match[1]
    elif _match := re.fullmatch( r"(.*?)(遅れ|行先変更|運休)がでています", text ):
        match _match[2]:
            case "遅れ":
                ret_status.enum = StatusEnum.DELAY
            case "行先変更":
                ret_status.enum = StatusEnum.DESTINATION_CHANGE
            case "運休":
                ret_status.enum = StatusEnum.SOME_TRAIN_CANCEL
            case _:
                pass
        modifier_text = _match[1]
    elif _match := re.fullmatch( r"(.*?)直通運転を中止しています", text ):
        ret_status.enum = StatusEnum.DIRECT_STOP
        modifier_text = _match[1]
    elif _match := re.fullmatch( r"(.*?)直通運転を再開しました", text ):
        ret_status.enum = StatusEnum.DIRECT_RESUMED
        modifier_text = _match[1]
    elif _match := re.fullmatch( r"(.*?)運転を見合わせています", text ):
        ret_status.enum = StatusEnum.OPERATION_STOP
        modifier_text = _match[1]
    elif _match := re.fullmatch( r"(.*?)運転を再開しました", text ):
        ret_status.enum = StatusEnum.OPERATION_RESUMED
        modifier_text = _match[1]
    elif _match := re.fullmatch( r"(.*?)折返し運転を行っています", text ):
        ret_status.enum = StatusEnum.TURN_BACK_OPERATION
        modifier_text = _match[1]
    elif _match := re.fullmatch( r"(.*?)の線路を使用し運転し(.+?)", text ):
        ret_status.enum = StatusEnum.ROUTE_CHANGE
        modifier_text = _match[1]
        if _match[2] == "、各駅に停車します":
            ret_snippet = Snippet(SnippetEnum.STOP_AT_EACH_STATION)
            for field in find_all_field(modifier_text):
                match field[0]:
                    case BetweenStations.header:
                        ret_snippet.sections.append(BetweenStations(field[1]))
    elif _match := re.fullmatch( r"(.*?)を中止しています", text ):
        ret_status.modifiers = gen_modifiers(_match[1])
        ret_status.enum = StatusEnum.STOP
        for other in ["女性専用車"]:
            if other in _match[1]:
                ret_status.modifiers[0].others.append(other)

    if modifier_text:
        ret_status.modifiers = gen_modifiers(modifier_text)

    return ret_status, ret_snippet

def gen_modifiers(text:str) -> list[StatusModifier]:

    ret: list[StatusModifier] = []

    for modifier_text in text.split("および"):
        modifier = StatusModifier()
        if "一部" in modifier_text:
            modifier.some_train = True
        if "現在も" in modifier_text:
            modifier.still = True
        for field in find_all_field(modifier_text):
            match field[0]:
                case LineName.header:
                    modifier.lines.append(LineName(field[1]))
                case BetweenStations.header:
                    modifier.sections.append(BetweenStations(field[1]))
                case OrdinalDirectionFromStation.header:
                    modifier.sections.append(OrdinalDirectionFromStation(field[1]))
                case Direction.header:
                    modifier.direction = Direction(field[1])
        if modifier:
            ret.append(modifier)
    if ret:
        return ret
    else:
        return [StatusModifier()]