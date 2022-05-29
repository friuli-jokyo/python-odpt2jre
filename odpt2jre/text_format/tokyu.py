
import copy
import odpttraininfo as odpt
from ..intermediate_components import *
from . import common
from .field_string import embed_field, find_all_field, find_field

staList = {
    "Tokyu.Oimachi":[["[Sta:119]","[Sta:5093]","[Sta:5094]","[Sta:5095]","[Sta:5096]","[Sta:5083]","[Sta:5097]","[Sta:5073]","[Sta:5098]","[Sta:5006]","[Sta:5099]","[Sta:5100]","[Sta:5101]","[Sta:5102]","[Sta:5034]","[Sta:5050]","[Sta:5051]","[Sta:5052]"]],
    "Tokyu.Toyoko":[["[Line:TokyoMetro.Fukutoshin]","[Sta:20]","[Sta:5001]","[Sta:5002]","[Sta:5003]","[Sta:5004]","[Sta:5005]","[Sta:5006]","[Sta:5013]","[Sta:5014]","[Sta:5015]","[Sta:151]","[Sta:5016]","[Sta:5017]","[Sta:5018]","[Sta:5019]","[Sta:196]","[Sta:5020]","[Sta:5021]","[Sta:5022]","[Sta:5023]","[Sta:126]","[Sta:5024]","[Sta:5025]","[Sta:5026]","[Sta:5027]","[Sta:5028]"]],
    "Tokyu.DenEnToshi":[["[Line:TokyoMetro.Hanzomon]","[Sta:20]","[Sta:5029]","[Sta:5030]","[Sta:5031]","[Sta:5032]","[Sta:5033]","[Sta:5034]","[Sta:5050]","[Sta:5051]","[Sta:5052]","[Sta:5053]","[Sta:5054]","[Sta:5055]","[Sta:5056]","[Sta:5057]","[Sta:5058]","[Sta:5059]","[Sta:5060]","[Sta:5061]","[Sta:5062]","[Sta:5063]","[Sta:202]","[Sta:5064]","[Sta:5065]","[Sta:5066]","[Sta:5067]","[Sta:5068]"]],
    "Tokyu.Meguro":[["[Line:Subway]","[Sta:22]","[Sta:5069]","[Sta:5070]","[Sta:5071]","[Sta:5072]","[Sta:5073]","[Sta:5074]","[Sta:5013]","[Sta:5014]","[Sta:5015]","[Sta:151]","[Sta:5016]","[Sta:5017]"]],
    "Tokyu.Ikegami":[["[Sta:23]","[Sta:5080]","[Sta:5081]","[Sta:5082]","[Sta:5083]","[Sta:5084]","[Sta:5085]","[Sta:5086]","[Sta:5087]","[Sta:5088]","[Sta:5089]","[Sta:5090]","[Sta:5091]","[Sta:5092]","[Sta:121]"]],
    "Tokyu.TokyuTamagawa":[["[Sta:5014]","[Sta:5075]","[Sta:5076]","[Sta:5077]","[Sta:94]","[Sta:5079]","[Sta:121]"]],
    "Tokyu.Setagaya":[["[Sta:5030]","[Sta:5111]","[Sta:5112]","[Sta:5113]","[Sta:5114]","[Sta:5115]","[Sta:5116]","[Sta:416]","[Sta:5117]","[Sta:4006]"]],
    "Tokyu.Kodomonokuni":[["[Sta:202]","[Sta:5118]","[Sta:5119]"]]
}

def to_jre(info:odpt.TrainInformation) -> list[TrainInformation]:

    if not info.train_information_status:
        return [common.normal_operation(info)]

    result:TrainInformation = TrainInformation(info)
    result.text_raw.ja = embed_field( info.train_information_text.ja )

    info_text = result.text_raw.ja

    if match := re.fullmatch( r".+?は、(.+?)の影響により、(.+?)。(.*)", info_text ):
        cause_text = match[1]
        main_status_text = match[2]
        sub_text_list = match[3].split("。")
    elif match := re.fullmatch( r".+?は、(.+?)。(.*)", info_text ):
        cause_text = ""
        main_status_text = match[1]
        sub_text_list = match[2].split("。")
    else:
        return [common.normal_operation(info)]

    if match := re.fullmatch( r"(.*?)運転を見合わせていましたが、(.*?)運転を再開(.+?)", main_status_text ):
        main_status_text = sub_text_list.pop(0)
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

    status_main, status_sub = text2status(main_status_text, info.get_line())
    if status_main:
        result.status_main = status_main
    if status_sub:
        result.statuses_sub.append(status_sub)

    for sub_text in sub_text_list:
        main_stat, sub_stat = text2status(sub_text, info.get_line())
        if main_stat:
            result.statuses_sub.append(main_stat)
        if sub_stat:
            result.statuses_sub.append(sub_stat)

    return [result]

def text2status(text:str, lineID:str) -> tuple[Optional[Status], Optional[Status]]:

    primary_status = Status(StatusPlacement.MAIN)
    secondary_status = None
    sub_status = False

    if "遅れ" in text or "運休" in text:
        if match := re.fullmatch( r"(.*?(遅れ|運休)と)(.+?)", text ):
            text = match[1]
            secondary_text = match[3]

            if "遅れ" in secondary_text:
                secondary_status = Status(StatusPlacement.MAIN)
                secondary_status.enum = StatusEnum.DELAY
            elif "運休" in secondary_text:
                sub_status = True
                secondary_status = Status(StatusPlacement.WITH)
                secondary_status.enum = StatusEnum.SOME_TRAIN_CANCEL

            if secondary_status:
                if "一部" in secondary_text:
                    secondary_status.modifiers[0].some_train = True

                for field in find_all_field(secondary_text):
                    match field[0]:
                        case Direction.header:
                            secondary_status.modifiers[0].direction = Direction(field[1])
                        case BetweenStations.header:
                            secondary_status.modifiers[0].sections.append(BetweenStations(field[1]))

    for field in find_all_field(text):
        match field[0]:
            case Direction.header:
                primary_status.modifiers[0].direction = Direction(field[1])
            case BetweenStations.header:
                primary_status.modifiers[0].sections.append(BetweenStations(field[1]))
            case LineName.header:
                primary_status.modifiers[0].lines.append(LineName(field[1]))

    if "一部" in text:
        primary_status.modifiers[0].some_train = True

    if "遅れ" in text:
        primary_status.enum = StatusEnum.DELAY
    elif "運休" in text:
        if "一部" in text or "Ｓトレイン" in text:
            primary_status.enum = StatusEnum.SOME_TRAIN_CANCEL
    elif "直通運転を中止" in text:
        primary_status.enum = StatusEnum.DIRECT_STOP
    elif "中止" in text:
        for other in ["女性専用車"]:
            if other in text:
                primary_status.enum = StatusEnum.STOP
                primary_status.modifiers[0].others.append(other)
    elif "行先変更" in text or "行き先変更" in text:
        primary_status.enum = StatusEnum.DESTINATION_CHANGE
    elif match := re.fullmatch( r"(.+?)で折返し運転を行っています", text):
        primary_status.enum = StatusEnum.OPERATION_STOP
        primary_status.modifiers[0].sections = []
        try:
            sections = copy.deepcopy(staList[ lineID ])
            formatted_text = re.sub(r"\[(SingleSta|BetweenSta):(.+?\])\]",r"\2",match[1]).replace("駅","").replace("間","").replace("内","")
            stopSections = [ re.split("[〜～\\,]",x) for x in formatted_text.split("、") ]

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
                section = [ s for s in section if "Line:" not in s ]
                if len(section)>1:
                    primary_status.modifiers[0].sections.append(BetweenStations("[BetweenSta:%s,%s]" %(section[0],section[-1])))
        except:
            pass

    else:
        return None, None

    if sub_status:
        primary_status.sub_status = secondary_status
        return primary_status, None
    else:
        return primary_status, secondary_status